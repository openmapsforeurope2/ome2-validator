from qgis.core import QgsWkbTypes, QgsSpatialIndex, QgsGeometry, QgsFeatureRequest, QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
from utilities import QgisUtilities

import logging

class NoAdjacentFacesSameAttributeValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, attributes: list[str]) -> list[ValidationResult]:
        """Runs the NoAdjacentFacesSameAttributeValidator.

        Checks if adjacent polygon features share the same attribute values.
        TODO ERM Validator has an additional AllowedSplittingFeatures parameter

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check. Must contain polygon-geometry.
            attributes (list[str]): A list of field-names.

        Returns:
            list[ValidationResult]: A list of results, containing the features which are adjacent to features sharing equal attribute values.
        """     
        results = []

        # Check geometry type
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.PolygonGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.PolygonGeometry])
            cls.logger.warning(log_message)
            return results

        # Check field existence
        for attribute in attributes:
            index = feature_class.fields().indexFromName(attribute)
            if index == -1:
                cls.logger.warning(f"Cannot run the {cls.__name__} on {feature_class.name()} for field {attribute} because the field does not exist.")
                return results
        
        plural = 's' if len(attributes) > 0 else ''
        attribute_subset = ['objectid'] + attributes
        
        # Create a dictionary of all features so we can compare attribute values later
        # TODO How will this scale to large datasets?
        request = QgsFeatureRequest().setSubsetOfAttributes(attribute_subset, feature_class.fields() )
        feature_dict = {f.id(): f for f in feature_class.getFeatures(request)}

        # Create index, store feature geometries so we can retrieve them later with index.geometry()
        index = QgsSpatialIndex(feature_class.getFeatures(), flags=QgsSpatialIndex.FlagStoreFeatureGeometries)

        # Loop over features
        for feature in feature_dict.values():
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

            # Check all candidate features for touch
            for candidate_id in candidate_ids:
                # Retrieve geometry via index
                g2 = index.geometry(candidate_id)
                if engine1.touches(g2.constGet()):
                    
                    # Check if the attributes are equal
                    feature2 = feature_dict[candidate_id]
                    equal_attributes = 0
                    all_fields = ', '.join(attributes)
                    all_values = ""
                    for attribute in attributes:
                        if feature[attribute] == feature2[attribute]:
                            if equal_attributes > 0:
                                all_values += ', '
                            all_values += f"'{feature[attribute]}'"
                            equal_attributes += 1

                    if len(attributes) == equal_attributes:
                        message = f"Features with objectid '{feature['objectid']}' and objectid '{feature2['objectid']}' are adjacent and share the same value{plural} {all_values} for field{plural} {all_fields}."
                        result = cls.create_result(run_id, validation_code, severity, feature_class, feature, message)
                        results.append(result)

        return results
