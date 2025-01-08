from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsWkbTypes, QgsSpatialIndex, QgsVectorLayer
from utilities import QgisUtilities
import logging

class MustBeCoveredByValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, feature_class_2: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the class MustBeCoveredByValidator.

        Topology validation for checking if points are covered by lines/areas.
        Based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L765

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class which should be covered. Must contain point-geometry.
            feature_class_2 (QgsVectorLayer): The feature class which is used for comparison. Must contain line- or polygon-geometry.

        Returns:
            list[ValidationResult]: A list of results, containing points of the point-featureclass which are not covered by the other featureclass.
        """
        results = []

        # Check geometry type
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.PointGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.PointGeometry])
            cls.logger.warning(log_message)
            return results
        if feature_class_2.geometryType() not in [QgsWkbTypes.GeometryType.LineGeometry, QgsWkbTypes.GeometryType.PolygonGeometry]:
            log_message = cls.get_invalid_geometry_type_message(feature_class_2, [QgsWkbTypes.GeometryType.LineGeometry, QgsWkbTypes.GeometryType.PolygonGeometry])
            cls.logger.warning(log_message)
            return results
        
        # Create index, store feature geometries so we can retrieve them later with index.geometry()
        index = QgsSpatialIndex(feature_class_2.getFeatures(), flags=QgsSpatialIndex.FlagStoreFeatureGeometries)
        
        # Loop over features
        for feature in feature_class.getFeatures():
            g1 = feature.geometry()

            # Check for valid geometry
            if QgisUtilities.is_empty_or_invalid_geometry(g1):
                log_message = cls.get_empty_or_invalid_geometry_message(feature_class, feature)
                cls.logger.warning(log_message)
                continue

            # Get all candidate features by intersecting against feature bounding box
            bb = g1.boundingBox()
            candidate_ids = index.intersects( bb )
            
            covered = False
            # Get all candidate features
            for candidate_id in candidate_ids:
                # Retrieve geometry via index
                g2 = index.geometry(candidate_id)

                # Check for valid geometry
                if QgisUtilities.is_empty_or_invalid_geometry(g2):
                    continue
                
                # Check if point is covered by a candidate feature
                # TODO Performance may be improved by using a GeometryEngine
                if g1.intersects(g2): # Use intersects for Covered By in stead of touch for Covered By Segment
                    covered = True
                    break
                
            if not covered:
                # Create feature of the non covered geometry
                feature_objectid = feature.attribute('objectid')
                error_feature = cls.create_error_feature(g1, feature_objectid)
                message = f'{feature_class.name()} object with objectid {feature.id()} is not covered by {feature_class_2.name()}.'
                result = cls.create_result(run_id, validation_code, severity, feature_class, error_feature, message)
                results.append(result)

        return results