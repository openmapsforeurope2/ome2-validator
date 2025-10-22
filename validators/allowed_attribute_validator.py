from fnmatch import fnmatch
from qgis.core import QgsFeatureRequest, QgsVectorLayer, QgsFeature
from models import ValidationResult
from . import FeatureValidator
from utilities import QgisUtilities
import logging

class AllowedAttributeValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id :int, validation_code: str, severity: str, feature_class: QgsVectorLayer, 
                 field_name: str, allowed_attributes: list[str], separator: str | None = None) -> list[ValidationResult]:
        """Runs the AllowedAttributeValidator.

        Checks for features which have a field value which is different than the allowed values.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            field_name (str): The name of the field to check.
            allowed_attributes (list[str]): The values which are allowed.
            separator (str): Optional separator used for splitting combined values, such as country = 'be#nl'. This defaults to None.

        Returns:
            list[ValidationResult]: A list of results, containing the features of which the specified field does not have an allowed value.
        """
        results = []

        if not QgisUtilities.layer_has_field(feature_class, field_name):
            cls.logger.warning(f"Cannot run the {cls.__name__} on {feature_class.name()} for field {field_name} because the field does not exist.")
            return results
        
        allowed_values, allowed_patterns = cls.get_allowed_values_and_patterns(allowed_attributes)

        allowed_attributes_quoted = [f"\'{attr}\'" for attr in allowed_values]
        allowed_attributes_list = f"({','.join(allowed_attributes_quoted)})"
        
        filter_expression = f'"{field_name}" not in {allowed_attributes_list}'
        
        if allowed_patterns:
            like_expressions = (
                f'"{field_name}" not like {pat}'
                for pat in allowed_patterns
            )
            filter_expression = (
                filter_expression 
                + ' and '
                + ' and '.join(like_expressions)
            )

        for feature in feature_class.getFeatures(QgsFeatureRequest().setFilterExpression(filter_expression)):
            field_value = feature.attribute(field_name)

            # Split values by separator when applicable
            country = cls.get_attribute(feature, 'country')
            if separator is not None and separator in field_value:
                split_values = field_value.split(separator)
                not_allowed = [
                    val for val in split_values 
                    if val not in allowed_values
                    and not any(fnmatch(val, pat) for pat in allowed_patterns)
                ]
                
                if len(not_allowed) > 0:
                    # Create error message for invalid values combined by a separator
                    message = cls.create_invalid_value_message(feature_class, feature, field_name)
                    result = cls.create_result(
                        run_id, validation_code, severity, feature_class, feature, message,
                        country
                    )
                    results.append(result)
                else:
                    # Create warning message for valid values combined by a separator
                    message = cls.create_valid_but_separator_message(feature_class, feature, field_name, separator)
                    result = cls.create_result(
                        run_id, validation_code, "WARNING", feature_class, feature, message,
                        country
                    )
                    results.append(result)
            else:
                # Create error message for invalid values without separator
                message = cls.create_invalid_value_message(feature_class, feature, field_name)
                result = cls.create_result(
                    run_id, validation_code, severity, feature_class, feature, message,
                    country
                )
                results.append(result)

        return results
    

    @classmethod
    def get_allowed_values_and_patterns(cls, allowed_attributes: list[str]) -> tuple[list[str], list[str]]:
        """Partitions a list of allowed attributes into two lists:
        one containing literal values and one containing wildcard patterns.

        Args:
            allowed_attributes (list[str]): the list of allowed attributes.

        Returns:
            tuple[list[str],list[str]]: a list of literal allowed attribute values and a list of allowed wildcard patterns.
        """
        attributes: list[str] = []
        patterns: list[str] = []

        for value in allowed_attributes:
            if '*' in value:
                patterns.append(value)
            else:
                attributes.append(value)

        return attributes, patterns
    
    @classmethod 
    def quote_pattern(cls, allowed_pattern: str) -> str:
        """Quotes a pattern such that it can be used in a filter expression.
        It escapes underscores and replaces the * wildcard symbol with %.

        Args:
            allowed_pattern (str): an allowed attribute pattern.

        Returns:
            str: the quoted pattern.
        """
        return allowed_pattern.replace('_', r'\_').replace('*', '%')
        

    @classmethod
    def create_invalid_value_message(cls, feature_class: QgsVectorLayer, feature: QgsFeature, field_name: str) -> str:
        """Creates a validation message for a feature containing an invalid attribute value.

        Args:
            feature_class (QgsVectorLayer): The feature class.
            feature (QgsFeature): The feature.
            field_name (str): The field name containing an invalid value

        Returns:
            str: An error message describing the invalid value.
        """        
        return f'{feature_class.name()} object with objectid \'{feature.attribute("objectid")}\' has an invalid value of \'{feature.attribute(field_name)}\' for field {field_name}.'


    @classmethod
    def create_valid_but_separator_message(cls,  feature_class: QgsVectorLayer, feature: QgsFeature, field_name: str, separator: str) -> str:
        """Creates a validation message for a feature containing a valid attribute value, but uses an incorrect separator.

        Args:
            feature_class (QgsVectorLayer): The feature class.
            feature (QgsFeature): The feature.
            field_name (str): The field name containing a valid value with a separator.
            separator (str): The corresponding separator.

        Returns:
            str: A warning message describing the usage of a separator.
        """        
        return f'{feature_class.name()} object with objectid \'{feature.attribute("objectid")}\' has a valid value of \'{feature.attribute(field_name)}\' for field {field_name} but uses {separator} as a separator.'
    