from qgis.core import QgsDistanceArea, QgsPointXY, QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
import logging
from typing import Union

class MinimumVertexDistanceValidator(FeatureValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, minimum_distance: Union[int, float] ) -> list[ValidationResult]:
        """Runs the MinimumVertexDistanceValidator.

        Checks if features contain geometry with consecutive vertices being closer together than the minimum_distance.

        TODO ERM Validator has a thresholdDistance, which prevents the reporting of vertices with a very small distance between them.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            minimum_distance (Union[int, float]): The minimum distance between vertices in meters.

        Returns:
            list[ValidationResult]: A list of results, containing the features which contain geometry with consecutive vertices being too closer together.
        """        
        results = []

        if type(minimum_distance) not in [int, float] or minimum_distance < 0:
            log_message = f"Skipping {cls.__name__} on '{feature_class.name()}' since the minimum_distance is not an int or float larger than 0."
            cls.logger.warning(log_message)
            return results

        d = QgsDistanceArea()
        for feature in feature_class.getFeatures():
            feature_results = []
            geom = feature.geometry()
            for part in geom.parts():
                part_vertices = [v for v in part.vertices()]
                for i in range(1, len(part_vertices)-1):
                    current_vertice = part_vertices[i]
                    next_vertice = part_vertices[i+1]
                    # conversion of QgsPoint to QgsPointXY is needed
                    distance = d.measureLine(QgsPointXY(current_vertice), QgsPointXY(next_vertice))

                    if distance < minimum_distance:
                        feature_results.append((current_vertice, next_vertice))
                        # TODO: Do we want to create a result containing the line between the vertices?
                        # feature = QgsFeature()
                        # line = QgsGeometry.fromPolyline([current_vertice, next_vertice])
                        # feature.setGeometry(line)

            for feature_result in feature_results:
                current_vertice, next_vertice = feature_result
                message = f'MinimumVertexDistance result for minimum distance: {minimum_distance}, between {current_vertice.asWkt()} and {next_vertice.asWkt()}'
                result = cls.create_result(run_id, validation_code, severity, feature_class, feature, message)
                results.append(result)

        return results
