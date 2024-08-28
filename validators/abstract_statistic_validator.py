from qgis.core import QgsVectorLayer
from abc import ABC
from . import AbstractValidator
from models import StatisticResult
from storage import StatisticResultRepository

class StatisticValidator(AbstractValidator, ABC):
    result_repository = StatisticResultRepository
    
    @classmethod
    def create_result(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, message: str) -> StatisticResult:
        """Creates a StatisticResult.

        Creates a StatisticResult which can be stored in the StatisticResultRepository.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class.
            message (str): A description of the statisical result.

        Returns:
            StatisticResult: A statistic result ready for database insertion.
        """        

        return StatisticResult(
            result_id = None,
            run_id = run_id,
            validation_code = validation_code,
            severity  = severity,
            feature_class = feature_class.name(),
            message = message
        )
