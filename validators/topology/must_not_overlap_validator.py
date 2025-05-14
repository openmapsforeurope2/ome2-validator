from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsGeometry, QgsSpatialIndex, QgsWkbTypes, QgsVectorLayer
from utilities import QgisUtilities
import logging

class MustNotOverlapValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, type_attributes: list[str] =[]) -> list[ValidationResult]:
        """Runs the class MustNotOverlapValidator.

        Topology validation for finding overlaps.
        Based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L342

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class which should not have overlap. Must contain polygon-geometry.
            type_attributes (list[str]): Optional list of attribute names that identify a subtype within the feature class.
                If specified, only overlapping features of the same type are marked as an error.

        Returns:
            list[ValidationResult]: A list of results, containing the geometry of overlapping areas.
        """
        results = []

        # Check geometry type
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.PolygonGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.PolygonGeometry])
            cls.logger.warning(log_message)
            return results

        # Create index, store feature geometries so we can retrieve them later with index.geometry()
        index = QgsSpatialIndex(feature_class.getFeatures(), flags=QgsSpatialIndex.FlagStoreFeatureGeometries)

        # Loop over features
        for feature in feature_class.getFeatures():
            g1 = feature.geometry()
            # Check for valid geometry
            if QgisUtilities.is_empty_or_invalid_geometry(g1):
                log_message = cls.get_empty_or_invalid_geometry_message(feature_class, feature)
                cls.logger.warning(log_message)
                continue

            # Create geometry engine for efficient testing of spatial relationships
            engine1 = QgsGeometry.createGeometryEngine(g1.constGet())
            engine1.prepareGeometry()

            # Get all candidate features by intersecting against feature bounding box
            bb = g1.boundingBox()
            candidate_ids = index.intersects( bb )

            # Don't compare feature against its own geometry
            if (feature.id() in candidate_ids):
                candidate_ids.remove(feature.id())

            # Check all candidate features for overlap
            for candidate_id in candidate_ids:
                # Retrieve geometry via index
                g2 = index.geometry(candidate_id)
                if engine1.overlaps(g2.constGet()):
                    overlapping_feature = feature_class.getFeature(candidate_id)
                    
                    same_type = True
                    for attribute_name in type_attributes:
                        if feature.attribute(attribute_name) != overlapping_feature.attribute(attribute_name):
                            same_type = False
                            break
                    
                    if same_type:
                        # Create feature of the overlapping geometry
                        error_geom = g1.intersection(g2)
                        error_feature = cls.create_error_feature(error_geom, feature['objectid'])
                        
                        message = f'{feature_class.name()} object with objectid {feature.attribute("objectid")} overlaps with object with objectid {overlapping_feature.attribute("objectid")}.'
                        result = cls.create_result(run_id, validation_code, severity, feature_class, error_feature, message)
                        results.append(result)

        return results
