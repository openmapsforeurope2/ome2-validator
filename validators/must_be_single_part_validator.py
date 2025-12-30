from qgis.core import QgsGeometry, QgsVectorLayer, QgsWkbTypes
from models import ValidationResult
from . import FeatureValidator
import logging

class MustBeSinglePartValidator(FeatureValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the MustBeSinglePartValidator.

        Checks if features contain multipart geometry.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.

        Returns:
            list[ValidationResult]: A list of results, containing the features which contain multipart geometry.
        """        
        results = []

        layer_type = feature_class.wkbType()

        if not QgsWkbTypes.isMultiType(layer_type):
            return results

        for feature in feature_class.getFeatures():
            geometry: QgsGeometry = feature.geometry()
            is_multipart = False
            number_of_parts = 1

            if geometry.type() == QgsWkbTypes.PolygonGeometry:
                parts = geometry.asMultiPolygon()
                is_multipart = len(parts) > 1
                number_of_parts = len(parts)

            elif geometry.type() == QgsWkbTypes.LineGeometry:
                parts = geometry.asMultiPolyline()
                is_multipart = len(parts) > 1
                number_of_parts = len(parts)

            elif geometry.type() == QgsWkbTypes.PointGeometry:
                parts = geometry.asMultiPoint()
                is_multipart = len(parts) > 1
                number_of_parts = len(parts)

            if is_multipart:
                message = f'{feature_class.name()} feature with objectid {(feature["objectid"])} is not a single part, has {number_of_parts} parts'
                country = cls.get_attribute(feature, 'country')
                result = cls.create_result(
                    run_id,
                    validation_code,
                    severity,
                    feature_class,
                    feature,
                    message,
                    country
                )
                results.append(result)

        return results
