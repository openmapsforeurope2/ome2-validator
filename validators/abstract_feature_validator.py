from qgis.core import QgsVectorLayer, QgsFeature
from abc import ABC
from . import AbstractValidator
from models import GeometryResult
from storage import GeometryResultRepository

class FeatureValidator(AbstractValidator, ABC):
    result_repository = GeometryResultRepository

    @classmethod
    def create_result(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, feature: QgsFeature, message: str) -> GeometryResult:
        """Creates a geometry result.

        Creates a GeometryResult which can be stored in the GeometryResultRepository.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class.
            feature (QgsFeature): The result feature containing the geometry and objectid
            message (str): A description of the geometry result.

        Returns:
            GeometryResult: A geometry result ready for database insertion.
        """        

        # Typed nulls for satisfying the typechecker
        GENERATE_ID: int = None  # type: ignore
        DETECT_TYPE: str = None # type: ignore

        return GeometryResult(
            result_id = GENERATE_ID,
            run_id = run_id,
            validation_code = validation_code,
            severity  = severity,
            feature_class = feature_class.name(),
            message = message,
            objectid = '00000000-0000-0000-0000-000000000000' if feature is None else feature['objectid'],
            geometry = None if feature is None else feature.geometry(),
            geometry_type = DETECT_TYPE
        )
