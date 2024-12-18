from typing import Optional, cast
from qgis.core import QgsVectorLayer, QgsFeature, QgsSpatialIndex, QgsWkbTypes
from models import ValidationResult
from . import FeatureValidator
from utilities import QgisUtilities
import logging



class MustTouchCorrespondingBoundaryValidator(FeatureValidator):
    logger = logging.getLogger(__name__)
    
    @classmethod
    def validate(cls, run_id :int, validation_code: str, severity: str, feature_class: QgsVectorLayer, 
                 area_feature_class: QgsVectorLayer, corresponding_attributes: list[str]) -> list[ValidationResult]:
        """Runs the MustTouchCorrespondingBoundaryValidator.

        Checks for features that do not touch the boundary of a corresponding feature in another feature class.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            area_feature_class (QgsVectorLayer): The corresponding feature class whose boundary must be touched.
            corresponding_attributes (list[str]): The attribute names, one for `feature_class` and one for `area_feature_class`,
                that indicate which features correspond to each other. For example: `['country', 'country']`.

        Returns:
            list[ValidationResult]: A list of results, containing the features that do not touch the boundary of a corresponding area feature.

        """        
        results = []
        exit_early = False

        # Unpack corresponding_attributes
        if len(corresponding_attributes) != 2:
            cls.logger.error('corresponding_attributes argument should contain 2 items')
            return results
        attribute_name_1, attribute_name_2 = corresponding_attributes

        # Check geometry types
        for fc in [feature_class, area_feature_class]:
            if fc.geometryType() != QgsWkbTypes.GeometryType.PolygonGeometry:
                log_message = cls.get_invalid_geometry_type_message(fc, [QgsWkbTypes.GeometryType.PolygonGeometry])
                cls.logger.warning(log_message)
                exit_early = True
        
        if exit_early:
            return results
        
        # Create index, store feature geometries so we can retrieve them later with index.geometry()
        index = QgsSpatialIndex(area_feature_class.getFeatures(), flags=QgsSpatialIndex.FlagStoreFeatureGeometries)

        # Loop over features
        for feature in cast(list[QgsFeature], feature_class.getFeatures()):
            g1 = feature.geometry()
            attribute_1 = feature.attribute(attribute_name_1)

            # Check for valid geometry
            if QgisUtilities.is_empty_or_invalid_geometry(g1):
                log_message = cls.get_empty_or_invalid_geometry_message(feature_class, feature)
                cls.logger.warning(log_message)
                continue

            # Get all candidate features by intersecting against feature bounding box
            bb = g1.boundingBox()
            candidate_ids = index.intersects(bb)
            touching_id: Optional[int] = None
            for candidate_id in candidate_ids:
                # Check if it is a corresponding feature based on attribute values
                feature2 = area_feature_class.getFeature(candidate_id)
                attribute_2 = feature2.attribute(attribute_name_2)
                if (attribute_1 != attribute_2):
                    continue

                # Retrieve geometry via index
                g2 = index.geometry(candidate_id)

                # Check for valid geometry
                if QgisUtilities.is_empty_or_invalid_geometry(g2):
                    continue
                
                # Perform touch check
                if g1.touches(g2):
                    touching_id = candidate_id
                    break
            
            if touching_id is None:
                error_geom = g1
                error_feature = cls.create_error_feature(error_geom, feature.attribute('objectid'))
                message = f'{feature_class.name()} object with objectid {feature.attribute("objectid")} and {attribute_name_1} {attribute_1} does not touch a corresponding feature from {area_feature_class.name()}'
                result = cls.create_result(run_id, validation_code, severity, feature_class, error_feature, message)
                results.append(result)

        return results
