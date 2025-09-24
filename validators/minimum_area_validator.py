from qgis.core import QgsDistanceArea, QgsWkbTypes, QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
import logging
from utilities import QgisUtilities

class MinimumAreaValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_classes:QgsVectorLayer | list[QgsVectorLayer], minimum_area: int | float) -> list[ValidationResult]:
        """Runs the MinimumAreaValidator.

        Checks if polygon features in the given featureclass are smaller than the minimum area.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_classes (Union[QgsVectorLayer, list[QgsVectorLayer]]): One or more featureclasses to check. Must contain polygon-geometry.
            minimum_area (Union[int, float]): The minimum area.

        Returns:
            list[ValidationResult]: A list of results, containing the features which are smaller than the minimum area.
        """        
        results: list[ValidationResult] = []
        
        # Parameter may be an array of QgsVectorLayers or a single one
        if type(feature_classes) is QgsVectorLayer:
            feature_classes = [feature_classes]
        
        if type(minimum_area) not in [int, float] or minimum_area < 0:
            log_message = f"Skipping {cls.__name__} on '{tuple(f.name() for f in feature_classes)}' since the minimum_area is not an int or float larger than 0."
            cls.logger.warning(log_message)
            return results

        d = QgsDistanceArea()

        for feature_class in feature_classes:

            # Check geometry type
            if feature_class.geometryType() != QgsWkbTypes.GeometryType.PolygonGeometry:
                log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.PolygonGeometry])
                cls.logger.warning(log_message)
                continue

            for feature in feature_class.getFeatures():
                
                # Check for valid geometry
                if QgisUtilities.is_empty_or_invalid_geometry(feature.geometry()):
                    log_message = cls.get_empty_or_invalid_geometry_message(feature_class, feature)
                    cls.logger.warning(log_message)
                    continue
                
                feature_area = d.measureArea(feature.geometry())
                if  feature_area < minimum_area:
                    message = f"Feature with objectid '{feature['objectid']}' has an area of {round(feature_area, 1)}m2 which is smaller than the minimum area of {minimum_area}m2."
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

