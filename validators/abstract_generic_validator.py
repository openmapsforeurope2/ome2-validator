from qgis.core import QgsVectorLayer
from abc import ABC
from . import AbstractValidator
from models import GenericResult
from storage import GenericResultRepository

class GenericValidator(AbstractValidator, ABC):
    result_repository = GenericResultRepository
    
    @classmethod
    def create_result(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, message: str) -> GenericResult:
        """Creates a GenericResult.

        Creates a GenericResult which can be stored in the GenericResultRepository.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class.
            message (str): A description of the generic result.

        Returns:
            GenericResult: A generic result ready for database insertion.
        """        

        return GenericResult(
            result_id = None,
            run_id = run_id,
            validation_code = validation_code,
            severity  = severity,
            feature_class = feature_class.name(),
            message = message
        )
