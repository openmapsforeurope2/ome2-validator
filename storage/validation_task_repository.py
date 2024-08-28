import pydapper

from models import ValidationTask
from typing import Union

class ValidationTaskRepository():
    dsn = None

    @classmethod
    def set_dsn(cls, dsn: str):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn


    @classmethod
    def add(cls, validation_task: ValidationTask):
        """Adds a new validation task to the repository.

        Args:
            validation_task (ValidationTask): The validation task.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                _ = commands.execute(
                    "INSERT INTO validation_task " +
                    "(name) " +
                    "VALUES (?name?)",
                    param = validation_task.as_param_dict()
                )
        finally:
            commands.connection.close()


    @classmethod
    def get_by_task_name(cls, task_name: str) -> Union[ValidationTask, None]:
        """Gets a validation task by task name.

        This method is used to determine if a validationtask is new or existing.
        If it exists, it is returned.

        Args:
            task_name (str): The task name.

        Returns:
            Union[ValidationTask, None]: The validation task with the given name, or None if it doesn't exist.
        """        
    
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                return commands.query_single_or_default(
                    "SELECT * FROM validation_task WHERE name = ?task_name?",
                    param = { "task_name": task_name},
                    model = ValidationTask,
                    default = None)
        finally:
            commands.connection.close()
