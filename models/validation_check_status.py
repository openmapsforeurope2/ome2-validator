from dataclasses import dataclass
from models import AbstractModel
import datetime

@dataclass
class ValidationCheckStatus(AbstractModel):
    """Dataclass for storing check statusses in the database.

    Attributes:
        validation_code (str): The validation code.
        run_id (int): The run id. Note that the combination of validation_code and run_id is unique for a ValidationCheckStatus.
        start_time (date): The start-time of this validation.
        end_time (date): The end-time of this validation.
        last_update (date): The time of the last-update of this validation.
        success (bool): Indicates if the corresponding validation ran successfully
    """
    validation_code: str
    run_id: int
    start_time: datetime.date
    end_time: datetime.date
    last_update: datetime.date
    success: bool
    number_of_results: int
