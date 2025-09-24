from qgis.core import QgsGeometry, QgsRectangle, QgsVectorLayer
from models import ValidationResult, BaseExtent
from . import FeatureValidator
import logging

class ExtentValidator(FeatureValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, extent: BaseExtent) -> list[ValidationResult]:
        """Runs the ExtentValidator.

        Checks if any features of the featureclass are not contained by the given extent.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            extent (BaseExtent): The extent to check against.

        Returns:
            list[ValidationResult]: A list of results, containing the features which are not contained by the extent.
        """        
        results = []

        # Create extent
        extent_rectangle = QgsGeometry.fromRect(QgsRectangle(extent.x_min, extent.y_min, extent.x_max, extent.y_max))

        # Check if entire layer is within the extent
        layer_extent = QgsGeometry.fromRect(feature_class.extent())
        if extent_rectangle.contains(layer_extent):
            return results
        
        # If not, check the individual features
        for feature in feature_class.getFeatures():
            if not extent_rectangle.contains(feature.geometry()):
                message = f'ExtentValidator result for extent: ({extent.x_min}, {extent.y_min}, {extent.x_max}, {extent.y_max})'
                country = cls.get_attribute(feature, 'country')
                result = cls.create_result(
                    run_id,
                    validation_code,
                    severity,
                    feature_class,
                    feature,
                    message,
                    country
                )
                results.append(result)

        return results
