

from qgis import processing
from qgis.core import QgsVectorLayer, QgsPoint, QgsWkbTypes
from models import ValidationResult
from . import FeatureValidator
import logging
from utilities import QgisUtilities
from qgis.PyQt.QtCore import QMetaType

from itertools import combinations

class AttributeAcrossBorderConsistencyValidator(FeatureValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, border_feature_class: QgsVectorLayer, consistent_attributes: list[str]) -> list[ValidationResult]:
        results = []
        orig_severity = severity

        # Check if there are field_names in the input
        if not consistent_attributes:
            log_message = f"Skipping {cls.__name__} on '{feature_class.name()}' since there are not attributes in the input."
            cls.logger.warning(log_message)
            return results
        
        # Check if the field name exists on the layer
        for field_name in consistent_attributes:
            if not QgisUtilities.layer_has_field(feature_class, field_name):
                log_message = f"Skipping {cls.__name__} on '{feature_class.name()}' for field {field_name} because the field does not exist."
                return results

        # Check geometry type, currently only line geometry is supported
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.LineGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.LineGeometry])
            cls.logger.warning(log_message)     
            return results

        prepared_feature_class = QgisUtilities.create_memory_layer(feature_class, skip_field_types = [QMetaType.QVariantMap])
        prepared_border_feature_class = QgisUtilities.create_memory_layer(border_feature_class, skip_field_types = [QMetaType.QVariantMap])
        
        poly_to_line_layer = "memory:poly_to_line_layer"
        
        # Convert border to lines
        parameters = {
            'INPUT': prepared_border_feature_class,
            'OUTPUT': poly_to_line_layer
        }

        polygons_to_lines = processing.run("native:polygonstolines", parameters)
        polygons_to_lines_layer = polygons_to_lines['OUTPUT']
        

        # Create buffer
        buffer_layer = "memory:buffer_layer"
        parameters = {
            'INPUT': polygons_to_lines_layer,
            'DISTANCE': 5,
            'SEGMENTS': 5,
            'END_CAP_STYLE': 0,
            'JOIN_STYLE': 0,
            'MITER_LIMIT': 2,
            'DISSOLVE': True,
            'OUTPUT': buffer_layer
        }

        buffer = processing.run("native:buffer", parameters)
        buffer_layer = buffer['OUTPUT']

        # Select features on border
        parameters = {
            'INPUT': prepared_feature_class,
            'PREDICATE': [0],
            'INTERSECT': buffer_layer,
            'METHOD': 0
        }

        buffer = processing.run("native:selectbylocation", parameters)

        # Store line endpoints including attribute values in dictionary
        border_point_dict = {}
        for feature in prepared_feature_class.selectedFeatures():

            # Get endpoints
            geom = feature.geometry().asPolyline()
            start_point = QgsPoint(geom[0])
            end_point = QgsPoint(geom[-1])
            
            # Get attribute values
            attr_values = []
            oid = feature['objectid']
            country = feature['country']
            attr_values.append(oid)
            attr_values.append(country)
            for attr in consistent_attributes:
                attr_values.append(feature[attr])

            for point in [start_point, end_point]:
                point_key = (point.x(), point.y())
                if point_key in border_point_dict:
                    border_point_dict[point_key].append(tuple(attr_values))
                else:
                    border_point_dict[point_key] = [tuple(attr_values)]

        # Skip points with less than 2 occurences
        border_point_dict = {key: value for key, value in border_point_dict.items() if len(value) > 1}

        # Check each point for attribute consistency
        for key, value in border_point_dict.items():
            x, y = key
            inconsistent_values = set()

            # Default severity is set to WARNING, in case of comparing to a VOID value
            severity = "WARNING"

            # Make combinations of lines connecting to this point
            combis = combinations(value, 2)
            for pair in combis:
                obj1, obj2 = pair
                
                # Skip combinations of the same country, we only check across the border
                if obj1[1] == obj2[1]:
                    continue

                # Compare the attributes that should be consistent
                for i in range(len(consistent_attributes)):
                    field_name = consistent_attributes[i]
                    val1 = obj1[i+2]
                    val2 = obj2[i+2]

                    if val1 != val2:
                        # The original severity is used only when the inconsistent attributes have real values (not 'void_unk' or 'void_*')
                        if not val1.startswith("void") and not val2.startswith("void"):
                            severity = orig_severity

                        val_list = [val1, val2]
                        val_list.sort()
                        concatenated_values = "|".join(val_list)
                        inconsistent_values.add((field_name, concatenated_values))

            if len(inconsistent_values) > 0:
                error_feature = cls.create_error_feature(QgsPoint(x, y))
                
                # Create error message
                message_list = []
                for incon_val in inconsistent_values:
                    field_name, joined_vals = incon_val
                    value1, value2 = joined_vals.split("|")
                    message = f"'{field_name}' changes from '{value1}' to '{value2}'"
                    message_list.append(message)
                messages = " and ".join(message_list)
                plural = "" if len(inconsistent_values) == 1 else "s"

                message = f'{feature_class.name()} has inconsistent attribute{plural} across the border, {messages}.'
                result = cls.create_result(run_id, validation_code, severity, feature_class, error_feature, message)
                results.append(result)

        return results
