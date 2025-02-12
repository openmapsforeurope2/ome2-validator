from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsPoint, QgsWkbTypes, QgsVectorLayer
from utilities import QgisUtilities
import logging

class MustNotHaveDanglesValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the class MustNotHaveDanglesValidator.

        Topology validation for finding dangling lines.
        Based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L139

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class which should not have dangles. Must contain line-geometry.

        Returns:
            list[ValidationResult]: A list of results, containing the endpoints of dangling lines.
        """
        results = []

        # Check geometry type
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.LineGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.LineGeometry])
            cls.logger.warning(log_message)          
            return results
        
        end_vertices_dict: dict[QgsPoint, list[int]] = {}
        
        # Loop over features
        for feature in feature_class.getFeatures():
            g1 = feature.geometry()
            # Check for valid geometry
            if QgisUtilities.is_empty_or_invalid_geometry(g1):
                log_message = cls.get_empty_or_invalid_geometry_message(feature_class, feature)
                cls.logger.warning(log_message)
                continue


            # Fill dict with polyline endpoints and corresponding feature id's
            for polyline in QgisUtilities.geometry_to_polyline_list(g1):
                start_point = polyline[0]
                end_point = polyline[-1]
                for point in [start_point, end_point]:
                    if point not in end_vertices_dict:
                        end_vertices_dict[point] = [feature.id()]
                    else:
                        end_vertices_dict[point].append(feature.id())

        for point, feature_ids in end_vertices_dict.items():
            # Endpoints which occur only once must be dangles
            repetitions = len(feature_ids)
            if repetitions == 1:
                error_geom = QgisUtilities.pointxy_to_geometry(point)
                feature = feature_class.getFeature(feature_ids[0])
                error_feature = cls.create_error_feature(error_geom, feature.attribute('objectid'))
                message = f'{feature_class.name()} object with objectid {feature.id()} has dangles.'
                result = cls.create_result(run_id, validation_code, severity, feature_class, error_feature, message)
                results.append(result)

        return results
