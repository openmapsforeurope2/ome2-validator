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
            record (logging.LogRecord): The log-record containg the information.
        """        
        log_record = ValidationLogging(log_id=None,
                                       timestamp=datetime.fromtimestamp(record.created),
                                       run_id=None,
                                       severity=record.levelname,
                                       message=record.msg,
                                       module=record.module)
        
        ValidationLoggingRepository.add(log_record)

