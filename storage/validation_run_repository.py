import pydapper

from models import ValidationRun

class ValidationRunRepository():
    dsn = None

    @classmethod
    def set_dsn(cls, dsn: str):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn


    @classmethod
    def add(cls, validation_run: ValidationRun):
        """Adds a new validation run to the repository.

        Args:
            validation_run (ValidationRun): The validation run.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                _ = commands.execute(
                    "INSERT INTO validation_run " +
                    "(task_id, parameters, in_progress, start_time) " +
                    "VALUES (?task_id?, ?parameters?, true, now())",
                    param = validation_run.as_param_dict()
                )
        finally:
            commands.connection.close()


    @classmethod
    def update_on_end(cls, validation_run: ValidationRun):
        """Updates the in_progress and end_time values for a validation-run.

        This should be called once a validation-run has finished.

        Args:
            validation_run (ValidationRun): The validationrun to be updated.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                _ = commands.execute(
                    "UPDATE validation_run " + 
                    "SET in_progress = false, end_time = now() " +
                    "WHERE run_id = ?run_id?",
                    param = validation_run.as_param_dict()
                )
        finally:
            commands.connection.close()


    @classmethod
    def get_latest_by_task_id(cls, task_id: int) -> ValidationRun:
        """Gets the latest validation run for the given task id.

        Args:
            task_id (int): The task id.

        Returns:
            ValidationRun: The latest validation run.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                return commands.query_single(
                    "SELECT * FROM validation_run WHERE task_id = ?task_id? ORDER BY run_id DESC LIMIT 1",
                    param = { "task_id": task_id},
                    model = ValidationRun)
        finally:
            commands.connection.close()
