from qgis.core import QgsGeometry, QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
import logging

class ValidGeometryValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the ValidGeometryValidator.

        Checks the geometric validity for each object in the given feature class.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.

        Returns:
            list[ValidationResult]: A list of results, containing the features which do not have valid geometry.
        """
        results = []

        for feature in feature_class.getFeatures():
            if not feature.geometry().isGeosValid():
                geom_errors = QgsGeometry.validateGeometry(feature.geometry(), QgsGeometry.ValidatorGeos)
                # TODO Log the specific geometry errors

                message = f'ValidGeometryValidator result for objectid: {feature["objectid"]}'
                result = cls.create_result(
                    run_id,
                    validation_code,
                    severity,
                    feature_class,
                    feature,
                    message,
                    cls.get_attribute(feature, 'country')
                )
                results.append(result)

        return results
