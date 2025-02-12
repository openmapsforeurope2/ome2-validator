from qgis.core import QgsVectorLayer, QgsWkbTypes
from models import ValidationResult
from . import FeatureValidator
import logging

class GeometryTypeValidator(FeatureValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, expected_geometry_type: str) -> list[ValidationResult]:
        """Runs the GeometryTypeValidator.

        Checks if the geometry of each feature in the featureclass is of the expected geometrytype.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The featureclass to check.
            expected_geometry_type (str): The expected geometrytype. This value should be an attribute of QgsWkbType

        Returns:
            list[ValidationResult]: A list of results, containing the features of which the geometry does not match the expected geometrytype.
        """
        results = []

        if not hasattr(QgsWkbTypes, expected_geometry_type):
            log_message = f"Skipping {cls.__name__} on '{feature_class.name()} since the expected geometrytype {expected_geometry_type} is not a known WkbType."
            cls.logger.warning(log_message)
            return results

        wkb_geom_type = getattr(QgsWkbTypes, expected_geometry_type)

        # Create a warning message if the geometry type of the layer is different than expected.
        if not feature_class.wkbType() == wkb_geom_type:
            log_message = f"The geometrytype of layer {feature_class.name()} is {QgsWkbTypes.displayString(feature_class.wkbType())} but is expected to be {QgsWkbTypes.displayString(wkb_geom_type)}."
            cls.logger.warning(log_message)

        # Check the geometry type of the individual features
        for feature in feature_class.getFeatures():
            feature_geom_type = feature.geometry().wkbType()
            if not feature_geom_type == wkb_geom_type:
                message = f"Feature with objectid '{feature['objectid']}' has geometrytype {QgsWkbTypes.displayString(feature_geom_type)} but is expected to be of type {QgsWkbTypes.displayString(wkb_geom_type)}."
                result = cls.create_result(run_id, validation_code, severity, feature_class, feature, message)
                results.append(result)

        return results
