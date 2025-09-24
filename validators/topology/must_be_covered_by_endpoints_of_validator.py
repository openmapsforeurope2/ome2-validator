from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsWkbTypes, QgsSpatialIndex, QgsVectorLayer
from utilities import QgisUtilities
import logging

class MustBeCoveredByEndpointsOfValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, feature_class_2: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the class MustBeCoveredByEndpointsOfValidator.\
        
        Topology validation for checking if points are covered by endpoints of lines.
        Based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L931

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class which should be covered by endpoints. Must contain point-geometry.
            feature_class_2 (QgsVectorLayer): The feature class which is used for comparison. Must contain line-geometry.

        Returns:
            list[ValidationResult]: A list of results, containing points of the point-featureclass which are not covered by an endpoint of the line-featureclass.
        """
        results = []

        # Check geometry type
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.PointGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.PointGeometry])
            cls.logger.warning(log_message)
            return results
        
        if feature_class_2.geometryType() != QgsWkbTypes.GeometryType.LineGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class_2, [QgsWkbTypes.GeometryType.LineGeometry])
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
            
            # Collect all points, necessary in case of multigeometry
            for point in QgisUtilities.geometry_to_point_list(g1):
                g1_singlepart = QgisUtilities.pointxy_to_geometry(point)
                
                # Get all candidate features by intersecting against feature bounding box
                bb = g1_singlepart.boundingBox()
                candidate_ids = index.intersects( bb )

                covered = False
                # Get all candidate features
                for candidate_id in candidate_ids:
                    # Retrieve geometry via index
                    g2 = index.geometry(candidate_id)

                    # Check for valid geometry
                    if QgisUtilities.is_empty_or_invalid_geometry(g2):
                        continue

                    # Collect all lines, necessary in case of multigeometry
                    polylines = []
                    if g2.isMultipart():
                        polylines.extend(g2.asMultiPolyline())
                    else:
                        polylines.append(g2.asPolyline())

                    for polyline in polylines:
                        # Look for intersections with endpoints
                        start_point_geom = QgisUtilities.pointxy_to_geometry(polyline[0])
                        end_point_geom = QgisUtilities.pointxy_to_geometry(polyline[-1])
                        covered = g1_singlepart.intersects(start_point_geom) or g1_singlepart.intersects(end_point_geom)

                        if covered:
                            break
                    
                if not covered:
                    # Create feature of the non covered geometry
                    error_feature = cls.create_error_feature(g1_singlepart, feature.attribute('objectid'))
                    message = f'{feature_class.name()} object with objectid {feature.id()} is not covered by an endpoint of {feature_class_2.name()}.'
                    country = cls.get_attribute(feature, 'country')
                    result = cls.create_result(
                        run_id,
                        validation_code,
                        severity,
                        feature_class,
                        error_feature,
                        message,
                        country
                    )
                    results.append(result)

        return results
