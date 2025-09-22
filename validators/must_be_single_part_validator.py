from qgis.core import QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
import logging

class MustBeSinglePartValidator(FeatureValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the MustBeSinglePartValidator.

        Checks if features contain multipart geometry.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.

        Returns:
            list[ValidationResult]: A list of results, containing the features which contain multipart geometry.
        """        
        results = []

        for feature in feature_class.getFeatures():
            if feature.geometry().isMultipart():
                message = f'{feature_class.name()} feature with objectid {(feature["objectid"])} is not a single part'
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
