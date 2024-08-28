from qgis.core import QgsGeometry, QgsRectangle, QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
import logging
from typing import Union

class ExtentValidator(FeatureValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, x_min: Union[int, float], y_min: Union[int, float], x_max: Union[int, float], y_max: Union[int, float]) -> list[ValidationResult]:
        """Runs the ExtentValidator.

        Checks if any features of the featureclass are not contained by the given extent.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            x_min (Union[int, float]): The min. x of the extent.
            y_min (Union[int, float]): The min. y of the extent.
            x_max (Union[int, float]): The max. x of the extent.
            y_max (Union[int, float]): The max. y of the extent.

        Returns:
            list[ValidationResult]: A list of results, containing the features which are not contained by the extent.
        """        
        results = []

        # Create extent
        extent = QgsGeometry.fromRect(QgsRectangle(x_min, y_min, x_max, y_max))

        # Check if entire layer is within the extent
        layer_extent = QgsGeometry.fromRect(feature_class.extent())
        if extent.contains(layer_extent):
            return results
        
        # If not, check the individual features
        for feature in feature_class.getFeatures():
            if not extent.contains(feature.geometry()):
                message = f'ExtentValidator result for extent: ({x_min}, {y_min}, {x_max}, {y_max})'
                result = cls.create_result(run_id, validation_code, severity, feature_class, feature, message)
                results.append(result)

        return results
