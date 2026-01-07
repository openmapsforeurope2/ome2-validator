from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsWkbTypes, QgsVectorLayer
from utilities import QgisUtilities
import logging

class MustNotHavePseudosValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer,  type_attributes: list[str] = []) -> list[ValidationResult]:
        """Runs the class MustNotHavePseudosValidator.

        Topology validation for finding pseudo-nodes in lines.
        Based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L613

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class which should not have pseudo-nodes.

        Returns:
            list[ValidationResult]: A list of results, containing points at the location of pseudo-nodes.
        """
        results = []

        # Check geometry type
        if feature_class.geometryType() != QgsWkbTypes.GeometryType.LineGeometry:
            log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.LineGeometry])
            cls.logger.warning(log_message)
            return results
        
        feature_cache = {}
        end_vertices_dict = {}

        # Loop over features
        for feature in feature_class.getFeatures():
            feature_cache[feature.id()] = feature
            g1 = feature.geometry()
            # Check for valid geometry
            if QgisUtilities.is_empty_or_invalid_geometry(g1):
                log_message = cls.get_empty_or_invalid_geometry_message(feature_class, feature)
                cls.logger.warning(log_message)
                continue

            # Fill dict with polyline endpoints and corresponding feature id's
            if g1.isMultipart():
                polylines = g1.asMultiPolyline()
            else:
                polylines = [g1.asPolyline()]

            for polyline in polylines:
                start_point = polyline[0]
                end_point = polyline[-1]
                end_vertices_dict.setdefault(start_point, []).append(feature.id())
                end_vertices_dict.setdefault(end_point, []).append(feature.id())

        for point, feature_ids in end_vertices_dict.items():
            # Endpoints which occur twice must be pseudo-nodes
            if len(feature_ids) != 2:
                continue

            feature1 = feature_cache[feature_ids[0]]
            feature2 = feature_cache[feature_ids[1]]

            has_same_attributes = all(
                feature1.attribute(attribute) == feature2.attribute(attribute)
                for attribute in type_attributes
            )

            if not has_same_attributes:
                continue

            error_geom = QgisUtilities.pointxy_to_geometry(point)

            error_feature = cls.create_error_feature(error_geom, feature1.attribute('objectid'))
            message = f'{feature_class.name()} contains a pseudo-node between objects with objectid\'s {feature1.attribute('objectid')} and {feature2.attribute('objectid')}.'
            country = cls.get_attribute(feature1, 'country')
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
