import logging
from storage import ValidationLoggingRepository
from models import ValidationLogging
from datetime import datetime

class PostgresHandler(logging.Handler):

    def __init__(self, level=0):
        super().__init__(level)


    def emit(self, record: logging.LogRecord):
        """The record is turned into a ValidationLogging object and added to the repository.

        Args:
            record (logging.LogRecord): The log-record containing the information.
        """        
        
        # Typed nulls for satisfying the typechecker
        GENERATE_ID: int = None  # type: ignore
        ID_SET_BY_REPOSITORY: int = None  # type: ignore

        log_record = ValidationLogging(log_id=GENERATE_ID,
                                       timestamp=datetime.fromtimestamp(record.created),
                                       run_id=ID_SET_BY_REPOSITORY,
                                       severity=record.levelname,
                                       message=record.msg,
                                       module=record.module)
        
        ValidationLoggingRepository.add(log_record)

