import os
import logging
from pathlib import Path
from typing import ClassVar
import pydapper
from dataclasses import dataclass
from storage import ValidationTaskRepository, ValidationRunRepository, GeometryResultRepository, GenericResultRepository, ValidationCheckStatusRepository, ValidationLoggingRepository

class StorageUtilities:
    logger = logging.getLogger(__name__)
    current_version = '0.2'
    dsn: ClassVar[str | None] = None

    SETTINGS_TABLE_NOT_FOUND = 'SETTINGS_TABLE_NOT_FOUND'
    SETTING_NOT_FOUND = 'SETTING_NOT_FOUND'


    @dataclass
    class ExistsResult:
         exists: bool


    @dataclass
    class SettingResult:
         value: str


    @classmethod
    def get_database_version(cls) -> str:
        """Gets the database version.

        Note that a warning message is returned when either the setting or the settings table could not be found.

        Returns:
            str: _description_
        """        
        if not cls.settings_table_exists():
             return cls.SETTINGS_TABLE_NOT_FOUND
        return cls.get_setting('version')


    @classmethod
    def settings_table_exists(cls) -> bool:
        """Checks if the settings table exists in the output database.

        Returns:
            bool: True if the table 'validation_settings' already exists.
        """
        if cls.dsn is None:
            raise Exception('Data Source Name (dsn) has not been set')
        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                return commands.query_single(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'validation_settings');",
                    model= cls.ExistsResult
                ).exists
        finally:
            commands.connection.close()


    @classmethod
    def get_setting(cls, setting_name: str) -> str:
        """Gets a value for the specified setting.

        Args:
            setting_name (str): The setting name.

        Returns:
            str: The value for the given setting name.
        """
        if cls.dsn is None:
            raise Exception('Data Source Name (dsn) has not been set')
        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                return commands.query_single_or_default(
                    "SELECT value AS value FROM validation_settings WHERE setting = ?setting_name?;",
                    param = { "setting_name": setting_name},
                    model= cls.SettingResult,
                    default = cls.SettingResult(cls.SETTING_NOT_FOUND)
                ).value
        finally:
            commands.connection.close()


    @classmethod
    def execute_sql_file(cls, sql_file: str):
        """Executes the given SQL file to the output database.

        Args:
            sql_file (str): The name of the SQL file to execute.
        """        
        if cls.dsn is None:
            raise Exception('Data Source Name (dsn) has not been set')
        
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        sql_file_path = os.path.join(os.path.dirname(curr_dir), 'sql', sql_file)
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                _ = commands.execute(Path(sql_file_path).read_text())
        finally:
            commands.connection.close()

    @classmethod
    def setup_repositories(cls, dsn: str):
        """Sets up the repositories and underlying database structure.

        Starts by retrieving the version of the current database structure.
        If its equal to the version of the validator, we don't need to run any additional SQL-scripts.
        If the settings table could not be found, we fully initialize the database structure by running 'init_db.sql'.
        If the settings table exists but the database version could not be determined, an error is raised.
        
        Future versions may contain incremental SQL-scripts, e.g., when going from version 0.1 to 0.2.
        Once we are sure that the database structure is up to date, then we set the DSN on all repositories.

        Args:
            dsn (str): The Data Source Name for the validation output

        Raises:
            RuntimeError: An error is thrown if the current database version could not be determined.
            RuntimeError: An error is thrown if the database version still doesn't match after trying to update it.
        """        
        cls.dsn = dsn
        database_version = cls.get_database_version()
        database_up_to_date: bool = False

        # Initialization
        if database_version == cls.current_version:
            database_up_to_date = True
        elif database_version == cls.SETTINGS_TABLE_NOT_FOUND:
            cls.execute_sql_file('init_db.sql')
            database_version = '0.1'
            database_up_to_date = database_version == cls.current_version
        elif database_version == cls.SETTING_NOT_FOUND:
            # This should never happen, the settings table is present but doesn't have a version value
            raise RuntimeError("Could not determine database version.")
        
        # Migration
        if not database_up_to_date:
            # convert version to tuple
            db_version_int = tuple(map(int, database_version.split('.')))

            if db_version_int < (0,2):
                cls.execute_sql_file('update_to_0.2.sql')
            if db_version_int < (0,3): 
                ... # cls.execute_sql_file('update_to_0.3.sql')
            
            database_up_to_date = True

        # Check for intermediate versions and run corresponding update-scripts here in future versions
        if (database_up_to_date):
            ValidationLoggingRepository.set_dsn(dsn)
            ValidationTaskRepository.set_dsn(dsn)
            ValidationRunRepository.set_dsn(dsn)
            GeometryResultRepository.set_dsn(dsn)
            GenericResultRepository.set_dsn(dsn)
            ValidationCheckStatusRepository.set_dsn(dsn)
        else:
            raise RuntimeError("Database version does not match validator version.")
