import pydapper

from models import ValidationCheckStatus

class ValidationCheckStatusRepository():
    dsn = None

    @classmethod
    def set_dsn(cls, dsn: str):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn


    @classmethod
    def add(cls, validation_check_status: ValidationCheckStatus):
        """Adds a new validation-checkstatus to the repository.

        This should be called before a validator's validation logic is started.

        Args:
            validation_check_status (ValidationCheckStatus): The checkstatus to be stored.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                _ = commands.execute(
                        "INSERT INTO validation_check_status " +
                        "(validation_code, run_id, start_time, last_update) " +
                        "VALUES (?validation_code?, ?run_id?, now(), now())",
                        param = validation_check_status.as_param_dict()
                    )
        finally:
            commands.connection.close()


    @classmethod
    def update_on_end(cls, validation_check_status: ValidationCheckStatus):
        """Updates the end_time, last_update and success value for a validation-checkstatus.

        This should be called after a validator's validation logic has finished, both in case of success or failure.

        Args:
            validation_check_status (ValidationCheckStatus): The checkstatus to be updated.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                _ = commands.execute(
                    "UPDATE validation_check_status " + 
                    "SET end_time = now(), last_update = now(), success = ?success? " +
                    "WHERE validation_code = ?validation_code? AND run_id = ?run_id?",
                    param = validation_check_status.as_param_dict()
                )
        finally:
            commands.connection.close()


    @classmethod
    def get_checks_by_run_id(cls, run_id: int, failed_only = False) -> list[ValidationCheckStatus]:
        """Gets all validation-checkstatusses by run id.

        This may be used to created an overview of all checks which have succeeded and/or failed for a specific run.

        Args:
            run_id (int): _description_
            failed_only (bool, optional): Option for only returning the failed checks. Defaults to False.

        Returns:
            list[ValidationCheckStatus]: A list of checkstatussen corresponding to the given run_id.
        """        
        failed_only_clause = "AND success = false" if failed_only else ""
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                return commands.query(
                    f"SELECT * FROM validation_check_status WHERE run_id = ?run_id? {failed_only_clause} ORDER BY start_time ASC",
                    param = { "run_id": run_id},
                    model = ValidationCheckStatus)
        finally:
            commands.connection.close()

