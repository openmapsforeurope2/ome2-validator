from __future__ import annotations

from collections import OrderedDict
import os
import json
from json import JSONEncoder
import pyjson5

class ValidationParameters:
    """Class for parsing and serializing validation parameters from and to JSON.

    ValidationParameters are parsed from a JSON-file by from_json().
    ValidationParameters can be serialized (without passwords) by to_json(), so they can be stored in the database as part of a ValidationRun.

    Attributes:
        specification (str): The ValidationSpecification on which these parameters are applicable.
        task_name (str): The task name.
        task_id (int): The task id.
        run_id (int): The run id.
        input_db_params (str): The database parameters which give access to the OME2 data which we want to validate.
        output_db_params (str): The database parameters which give access to database where we want to write the validation output.
        themes (list[str]): A selection of themes which we want to validate.
        checks (list[str]): A selection of checks which we want to validate.
        groups list[str]: A selection of country-groups which we want to validate.
        countries (list[str]): A selection of countries which we want to validate.
        min_required_only (bool): An option to run only th minimum required checks.
    """
    specification: str
    task_name: str
    task_id: int
    run_id: int
    input_db_params: DatabaseConnectionParameters
    output_db_params: DatabaseConnectionParameters
    themes: list[str]
    checks: list[str]
    groups: list[str]
    countries: list[str]
    min_required_only: bool

    def __init__(self):
        self.task_id = None # type: ignore
        self.run_id = None # type: ignore
        self.input_db_params = self.DatabaseConnectionParameters()
        self.output_db_params = self.DatabaseConnectionParameters()

    @classmethod
    def get_example_json(cls) -> str:
        """Returns example validation parameters.

        Returns:
            str: Example validation parameters in JSON format.
        """
        return json.dumps(OrderedDict(
            specification='DV1',
            task_name='Validation on OME2 data',
            input_database=OrderedDict(
                host='my-postgis-db.postgres.database.azure.com',
                port=5432,
                name='ome2_db',
                username='postgres',
                password='postgres'
            ),
            output_database=OrderedDict(
                host='host.docker.internal',
                port=5432,
                name='ome2_validation_results',
                username='postgres',
                password='postgres'
            ),
            themes=['ADMINSTRATIVE_UNITS'],
            checks=[],
            groups=[],
            countries=['NL'],
            min_required_only=False
            ), indent=4
        )
        

    @classmethod
    def from_json(cls, json_filename: str) -> ValidationParameters:
        """Parses info from a JSON file into a ValidationParameters object.

        Args:
            json_filename (str): The name of the JSON-file which contains the validation parameters.

        Returns:
            ValidationParameters: the validation parameters parsed into the model.
        """
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(os.path.dirname(curr_dir), json_filename)
        
        with open(path, "r", encoding="utf8") as json_params_text:
            json_params = pyjson5.decode_io(json_params_text, maxdepth=None, some=False) # type: ignore
            
            params = ValidationParameters()
            params.specification = json_params.get("specification")
            params.task_name = json_params.get("task_name")

            for db_prop, db_json_key in [(params.input_db_params, "input_database"), (params.output_db_params, "output_database")]:
                db_params = json_params.get(db_json_key)
                if db_params:
                    db_prop.host = db_params.get('host')
                    db_prop.port = db_params.get('port')
                    db_prop.name = db_params.get('name')
                    db_prop.username = db_params.get('username')
                    db_prop.password = db_params.get('password')

            params.themes = json_params["themes"]
            params.checks = json_params["checks"]
            params.groups = json_params["groups"]
            params.countries = json_params["countries"]
            params.min_required_only = json_params["min_required_only"]
            return params
        
    def are_complete(self) -> bool:
        """Checks if the validation parameters are complete.

        Returns:
            bool: True if all necessary attributes could be parsed from the JSON file.
        """        
        return bool(
            self.specification and
            self.task_name and
            self.input_db_params.are_complete() and
            self.output_db_params.are_complete() and
            self.themes is not None and
            self.checks is not None and
            self.groups is not None and
            self.countries is not None and
            self.min_required_only is not None
            )

    def to_json(self) -> str:
        """Converts the object into a JSON string using an encoder.

        Returns:
            str: A JSON string, ready to be stored in the database
        """        
        return json.dumps(self, cls=self.ValidationParametersEncoder, indent=4)
    

    def theme_is_enabled(self, theme_name: str) -> bool:
        """Determines if a theme is enabled, based on the theme name and validation parameters.
        
        Note: This check only considers the first 5 characters.

        Returns:
            bool: True if the theme is enabled.
        """
        if len(self.themes) == 0:
            return True
        return theme_name in [t[:5].upper() for t in self.themes]
    

    def check_is_enabled(self, validation_code: str) -> bool:
        """Determines if a check is enabled, based on the validation code and validation parameters.

        Returns:
            bool: True if the check is enabled.
        """
        if len(self.checks) == 0:
            return True
        
        # I.e. ["T001"] will enable both T001a and T001b
        return validation_code.startswith(tuple(self.checks))
    

    class DatabaseConnectionParameters():
        host: str
        port: int
        name: str
        username: str
        password: str

        def are_complete(self) -> bool:
            """Checks if the database connection parameters are complete.

            Returns:
                bool: True if all necessary attributes could be parsed from the JSON file.
            """            
            return bool(self.host and self.name and self.username and self.password)

        def create_pg_dsn(self) -> str:
            """Create a Data Source Name

            Returns:
                str: the Data Source Name
            """            
            port_string = "" if self.port is None else f":{self.port}"
            return f"postgresql://{self.username}:{self.password}@{self.host}{port_string}/{self.name}"

    class ValidationParametersEncoder(JSONEncoder):
        """A custom encoder for the ValidationParameters, which prevents the storage of passwords in the database.
        """
        def default(self, o: object) -> dict:
            """Creates a serializable object, without any passwords if it is of type ValidationParameters.

            Args:
                o (object): the object to be serialized, we expect it to be of type ValidationParameters.

            Returns:
                __dict__: the serializable object
            """          
            output_dict = dict(o.__dict__)
            if isinstance(o, ValidationParameters.DatabaseConnectionParameters):
                # Remove DB passwords
                del output_dict['password']

            return output_dict
