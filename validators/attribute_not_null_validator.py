from qgis.core import QgsFeatureRequest, QgsVectorLayer, QgsExpression
from models import ValidationResult
from . import FeatureValidator
from utilities import QgisUtilities
import logging

class AttributeNotNullValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, field_name: str) -> list[ValidationResult]:
        """Runs the AttributeNotNullValidator.

        Checks if features in the given featureclass have NULL values for the specified field.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            field_name (str): The name of the field to check

        Returns:
            list[ValidationResult]: A list of results, containing the features of which the specified field has a NULL value.
        """        
        results = []

        # Check field existence
        if not QgisUtilities.layer_has_field(feature_class, field_name):
            cls.logger.warning(f"Cannot run the {cls.__name__} on {feature_class.name()} for field {field_name} because the field does not exist.")
            return results
        
        is_null_expression = f'"{field_name}" is NULL'

        if not QgsExpression(is_null_expression).isValid():
            log_message = f"Skipping {cls.__name__} on '{feature_class.name()}' as the following expression is not valid: {is_null_expression}"
            cls.logger.warning(log_message)
            return results

        for feature in feature_class.getFeatures(QgsFeatureRequest().setFilterExpression(is_null_expression)):
            message = f'{feature_class.name()} object with objectid {feature.attribute("objectid")} has a NULL value for field {field_name}.'
            result = cls.create_result(
                run_id,
                validation_code,
                severity,
                feature_class,
                feature,
                message,
                cls.get_attribute(feature, 'country')
            )
            results.append(result)

        return results
