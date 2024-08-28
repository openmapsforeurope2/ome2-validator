from dataclasses import dataclass
from models import AbstractModel
import datetime

@dataclass
class ValidationRun(AbstractModel):
    """Dataclass for storing validation runs in the database.

    Attributes:
        run_id (int): The id of this validation run, automatically generated for new tasks by the database on insertion.
        task_id (str): The id of the corresponding validation task.
        parameters (str): The validation parameters used to start this validation run. Note that database passwords are removed before storage.
        start_time (date): The start-time of this validation run.
        end_time (date): The end-time of this validation run.
        in_progress (bool): Indicates wether this validation run is still in progress.
    """
    run_id: int
    task_id: int
    parameters: str
    start_time: datetime.date
    end_time: datetime.date
    in_progress: bool
