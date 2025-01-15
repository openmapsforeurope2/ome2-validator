from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsWkbTypes, QgsSpatialIndex, QgsVectorLayer
from utilities import QgisUtilities
import logging

class EndPointsMustBeCoveredByValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, feature_class_2: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the EndPointsMustBeCoveredByValidator.

        Topology validation for checking if endpoints of lines are covered by points.
        Based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L1005

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class of which the endpoints should be covered. Must contain line-geometry.
            feature_class_2 (QgsVectorLayer): The feature class which is used for comparison. Must contain point-geometry.

        Returns:
            list[ValidationResult]: A list of results, containing the endpoints of the line-featureclass which are not covered by the point-featureclass.
        """
        results = []

        # Check geometry type
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.LineGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.LineGeometry])
            cls.logger.warning(log_message)
            return results
    
        if feature_class_2.geometryType() != QgsWkbTypes.GeometryType.PointGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class_2, [QgsWkbTypes.GeometryType.PointGeometry])
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

            # Collect all lines, and then collect all their endpoints
            endpoints = []
            for polyline in QgisUtilities.geometry_to_polyline_list(g1):
                start_point_geom = QgisUtilities.pointxy_to_geometry(polyline[0])
                end_point_geom = QgisUtilities.pointxy_to_geometry(polyline[-1])
                endpoints.append(start_point_geom)
                endpoints.append(end_point_geom)
            
            for endpoint in endpoints:
                bb = endpoint.boundingBox()
                candidate_ids = index.intersects( bb )

                covered = False
                for candidate_id in candidate_ids:
                    # Retrieve geometry via index
                    g2 = index.geometry(candidate_id)

                    # Check for valid geometry
                    if QgisUtilities.is_empty_or_invalid_geometry(g2):
                        continue

                    if g2.intersects(endpoint):
                        covered = True
                        break

                if not covered:
                    # Create feature of the non covered geometry
                    error_feature = cls.create_error_feature(endpoint, feature.attribute('objectid'))
                    message = f'{feature_class.name()} object with objectid {feature.id()} has an endpoint which is not covered by {feature_class_2.name()}.'
                    result = cls.create_result(run_id, validation_code, severity, feature_class, error_feature, message)
                    results.append(result)

        return results
