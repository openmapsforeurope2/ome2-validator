from dataclasses import dataclass
from models import AbstractModel

@dataclass
class ValidationResult(AbstractModel):
    """Abstract dataclass for storing validation results in the database.

    Attributes:
        result_id (int): The id of this validation result, automatically generated for new results by the database on insertion.
        run_id (str): The id of the corresponding validation run.
        validation_code (str): The validation code for this result.
        severity (str): The severity of this result (WARNING / ERROR / STATISTIC).
        feature_class (str): The corresponding feature_class.
        message (str): The message for this result.
    """
    result_id: int
    run_id: int
    validation_code: str
    severity: str
    feature_class: str
    message: str
