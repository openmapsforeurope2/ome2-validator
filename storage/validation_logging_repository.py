from typing import ClassVar
import pydapper

from models import ValidationLogging

class ValidationLoggingRepository():
    dsn: ClassVar[str | None] = None
    __current_run_id: ClassVar[int | None] = None

    @classmethod
    def set_dsn(cls, dsn: str):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn

    @classmethod
    def set_current_run_id(cls, current_run_id: int):
        """Sets the current run id so it can be used in consecutive logging.

        Args:
            current_run_id (int): The current run id
        """        
        cls.__current_run_id = current_run_id


    @classmethod
    def add(cls, validation_logging: ValidationLogging):
        """Adds a log-record to the log table.

        Calling this method is the responsibility of the PostgresHandler.

        Args:
            validation_logging (ValidationLogging): The logging to be stored.
        """ 
        if cls.dsn is None:
            raise Exception('Data Source Name (dsn) has not been set')
               
        validation_logging.run_id = cls.__current_run_id
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                _ = commands.execute(
                    "INSERT INTO validation_logging " +
                    "(timestamp, run_id, severity, message, module) " +
                    "VALUES (?timestamp?, ?run_id?, ?severity?, ?message?, ?module?)"
                    ,
                    param = validation_logging.as_param_dict()
                )
        finally:
            commands.connection.close()
