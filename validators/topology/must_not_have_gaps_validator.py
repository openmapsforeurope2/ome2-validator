from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsGeometry, QgsWkbTypes, QgsVectorLayer
from utilities import QgisUtilities
import logging

class MustNotHaveGapsValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the class MustNotHaveGapsValidator.

        Topology validation for finding gaps.
        Somewhat based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L467

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class which should not have gaps. Must contain polygon-geometry.

        Returns:
            list[ValidationResult]: A list of results, containing the geometry of the gaps.
        """
        results = []

        # Check geometry type
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.PolygonGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.PolygonGeometry])
            cls.logger.warning(log_message)
            return results
        
        # Create union of all geometries
        union = QgsGeometry.unaryUnion([f.geometry() for f in feature_class.getFeatures()])
        
        # Determine the gaps
        union_without_gaps = union.removeInteriorRings()
        gaps = union_without_gaps.difference(union)

        for gap in gaps.parts():
            error_geom = QgisUtilities.polygon_to_geometry(gap)
            error_feature = cls.create_error_feature(error_geom)
            message = f'{feature_class.name()} should not have this gap.'
            result = cls.create_result(run_id, validation_code, severity, feature_class, error_feature, message)
            results.append(result)

        return results
