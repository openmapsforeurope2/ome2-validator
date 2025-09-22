from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsWkbTypes, QgsSpatialIndex, QgsVectorLayer
from utilities import QgisUtilities
import logging

class MustContainValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, feature_class_2: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the class MustContainValidator.

        Topology validation for checking if polygons contain points.
        Based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L1181

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class which should contain. Must contain polygon-geometry.
            feature_class_2 (QgsVectorLayer): The feature class which is used for comparison. Must contain point-geometry.

        Returns:
            list[ValidationResult]: A list of results, containing the polygons of the polyon-featureclass which do not contain any point.
        """
        results = []

        # QGIS TopologyChecker only supports Polygon contains Point, but this validator could be more generic

        # Check geometry type
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.PolygonGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.PolygonGeometry])
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

            # Get all candidate features by intersecting against feature bounding box
            bb = g1.boundingBox()
            candidate_ids = index.intersects( bb )

            contains = False
            # Get all candidate features
            for candidate_id in candidate_ids:
                # Retrieve geometry via index
                g2 = index.geometry(candidate_id)

                # Check for valid geometry
                if QgisUtilities.is_empty_or_invalid_geometry(g2):
                    continue

                if g1.contains(g2):
                    contains = True
                    break
            
            if not contains:
                # Create feature of the geometry which does not contain another feature
                error_feature = cls.create_error_feature(g1, feature.attribute('objectid'))
                message = f'{feature_class.name()} object with objectid {feature.id()} does not contain a feature of {feature_class_2.name()}.'
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
