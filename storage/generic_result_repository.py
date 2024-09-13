import pydapper

from models import GenericResult

class GenericResultRepository():
    dsn = None
    
    @classmethod
    def set_dsn(cls, dsn: str):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn


    @classmethod
    def add(cls, validation_result: GenericResult):
        """Adds a single GenericResult to the repository.

        Args:
            validation_result (GenericResult): The generic result to be stored.
        """        
        cls.add_list([validation_result])


    @classmethod
    def add_list(cls, generic_results: list[GenericResult]):
        """Adds multiple GenericResults to the repository.

        Args:
            generic_results (list[GenericResult]): The generic results to be stored.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                for validation_result in generic_results:
                    _ = commands.execute(
                        "INSERT INTO generic_result " +
                        "(run_id, validation_code, severity, feature_class, message) " +
                        "VALUES (?run_id?, ?validation_code?, ?severity?, ?feature_class?, ?message?)",
                        param = validation_result.as_param_dict()
                    )
        finally:
            commands.connection.close()


    @classmethod
    def get_by_run_id(cls, run_id: int) -> list[GenericResult]:
        """Gets all GenericResults for the validation-run with the given run_id.

        Args:
            run_id (int): The run id.

        Returns:
            list[GenericResult]: All generic results for the corresponding run.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                return commands.query(
                    "SELECT * FROM generic_result WHERE run_id = ?run_id? ORDER BY result_id ASC",
                    param = { "run_id": run_id},
                    model = GenericResult)
        finally:
            commands.connection.close()
