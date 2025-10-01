from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QVariant
from models import ValidationResult
from . import GenericValidator
from utilities import QgisUtilities
import logging

class FeatureCountValidator(GenericValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, group_by_field_1: str | None = None, group_by_field_2: str | None = None, minimum_record_count: int = -1) -> list[ValidationResult]:
        """Runs the FeatureCountValidator

        Check if a featureclass has less features than the minimum record count.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            group_by_field_1 (str): A group by field. Defaults to None.
            group_by_field_2 (str): A second group by field. Defaults to None
            minimum_record_count (int): Minimum number of records. Defaults to -1.

        Returns:
            list[ValidationResult]: A list of 0 or 1 results, describing the feature count for this featureclass.
        """
        results = []

        if group_by_field_1 and not QgisUtilities.layer_has_field(feature_class, group_by_field_1):
            cls.logger.warning(cls.create_field_doesnt_exist_message(feature_class, group_by_field_1))
            return results
        
        if group_by_field_2 and not QgisUtilities.layer_has_field(feature_class, group_by_field_2):
            cls.logger.warning(cls.create_field_doesnt_exist_message(feature_class, group_by_field_2))
            return results
        
        if group_by_field_2 and not group_by_field_1:
            log_message = f"Skipping {cls.__name__} on '{feature_class.name()}' since a second groupby-field cannot be used without a first groupby-field."
            cls.logger.warning(log_message)
            return results

        # Create and collect all expressions
        expressions: list[str | None] = []
        expression2country: dict[str, str] = {}
        if not group_by_field_1 and not group_by_field_2:
            expressions.append(None)
        else:
            for val_1 in cls.get_unique_values(feature_class, group_by_field_1):
                field1_is_country = group_by_field_1 == 'country'
                field2_is_country = group_by_field_2 == 'country' 

                exp1 = cls.get_equals_expression(group_by_field_1, val_1)
                if not group_by_field_2:
                    expressions.append(exp1)
                    if field1_is_country:
                        expression2country[exp1] = val_1
                else:
                    for val_2 in cls.get_unique_values(feature_class, group_by_field_2):
                        exp2 = cls.get_equals_expression(group_by_field_2, val_2)
                        combined_exp = f'{exp1} AND {exp2}'
                        expressions.append(combined_exp)
                        if field1_is_country:
                            expression2country[combined_exp] = val_1
                        elif field2_is_country:
                            expression2country[combined_exp] = val_2
        
        # Peform feature counts and create results
        for exp in expressions:
            feature_count = None
            country = None

            if exp is None:
                feature_count = feature_class.featureCount()
            else:
                feature_class.selectByExpression(exp)
                feature_count = feature_class.selectedFeatureCount()
                country = expression2country.get(exp, None)
            
            if feature_count < minimum_record_count or minimum_record_count == -1:
                message = cls.create_featurecount_message(feature_class, feature_count, exp)
                result = cls.create_result(
                    run_id,
                    validation_code,
                    severity,
                    feature_class,
                    message,
                    country
                )
                results.append(result)
            
        return results
    

                

    @classmethod
    def create_field_doesnt_exist_message(cls, feature_class, group_by_field) -> str:
        return f"Skipping {cls.__name__} on '{feature_class.name()}' for field {group_by_field} because the field does not exist."


    @classmethod
    def get_equals_expression(cls, field, value) -> str:
        if type(value) is QVariant and value.isNull():
            return f'"{field}" is {value}'
        return f'"{field}" = \'{value}\''


    @classmethod
    def create_featurecount_message(cls, feature_class, feature_count, expression) -> str:
        expression_part = ""
        if expression:
            expression_part = f" for {expression}"
        plural = "" if feature_count == 1 else "s"
        return f"Featureclass '{feature_class.name()}' has {feature_count} record{plural}{expression_part}."
    

    @classmethod
    def get_unique_values(cls, feature_class, field_name) -> list[str]:
        field_index = feature_class.fields().indexFromName(field_name) 
        return sorted(feature_class.uniqueValues(field_index))
