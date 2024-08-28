import pydapper

from models import StatisticResult

class StatisticResultRepository():
    dsn = None
    
    @classmethod
    def set_dsn(cls, dsn: str):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn


    @classmethod
    def add(cls, validation_result: StatisticResult):
        """Adds a single StatisticResult to the repository.

        Args:
            validation_result (StatisticResult): The statistic result to be stored.
        """        
        cls.add_list([validation_result])


    @classmethod
    def add_list(cls, statistic_results: list[StatisticResult]):
        """Adds multiple StatisticResults to the repository.

        Args:
            statistic_results (list[StatisticResult]): The statistic results to be stored.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                for validation_result in statistic_results:
                    _ = commands.execute(
                        "INSERT INTO statistic_result " +
                        "(run_id, validation_code, severity, feature_class, message) " +
                        "VALUES (?run_id?, ?validation_code?, ?severity?, ?feature_class?, ?message?)",
                        param = validation_result.as_param_dict()
                    )
        finally:
            commands.connection.close()


    @classmethod
    def get_by_run_id(cls, run_id: int) -> list[StatisticResult]:
        """Gets all StatisticResults for the validation-run with the given run_id.

        Args:
            run_id (int): The run id.

        Returns:
            list[StatisticResult]: All statistic results for the corresponding run.
        """        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                return commands.query(
                    "SELECT * FROM statistic_result WHERE run_id = ?run_id? ORDER BY result_id ASC",
                    param = { "run_id": run_id},
                    model = StatisticResult)
        finally:
            commands.connection.close()
