import logging
from .log_handlers import PostgresHandler

class LogUtilities:

    __logger = None
    VERBOSE = 5
    is_configured = False

    @classmethod
    def configure_logging(cls, level=logging.DEBUG):
        """Configures the logging by settings the PostgresHandler and adding the verbose loglevel.

        Args:
            level (int, optional): The log level. Defaults to logging.DEBUG.
        """
        # Should only be ran once
        if cls.is_configured:
            return

        # Set config and add handler on root logger
        cls.__logger = logging.getLogger()
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S',
                            level=level)

        # Setup VERBOSE log level, do we really need this?
        # Module is always set to 'log_utilities' for verbose logging..
        if not logging.getLevelName(cls.VERBOSE) == "VERBOSE":
            logging.VERBOSE = cls.VERBOSE
            logging.addLevelName(logging.VERBOSE, "VERBOSE")
            logging.Logger.verbose = lambda inst, msg, *args, **kwargs: inst.log(logging.VERBOSE, msg, *args, **kwargs)
            logging.verbose = lambda msg, *args, **kwargs: logging.log(logging.VERBOSE, msg, *args, **kwargs)

        postgres_handler = PostgresHandler()
        postgres_handler.setLevel(logging.DEBUG)
        cls.__logger.addHandler(postgres_handler)
        cls.is_configured = True
