from qgis.core import QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
import logging
from utilities import QgisUtilities


class DebugFeatureValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the DebugFeatureValidator.

        This validator is for developers for iterating through features, setting breakpoints and performing various tests.
        
        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The featureclass to check.

        Returns:
            list[ValidationResult]: A list of unspecified results.
        """        
        results = []
        cls.logger.info("DebugFeatureValidator")

        for feature in feature_class.getFeatures():
            # For developers: add code and set breakpoints
            pass
        
        return results
