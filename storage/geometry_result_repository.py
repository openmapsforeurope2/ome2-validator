import sys
from typing import ClassVar
import pydapper

from models import GeometryResult
from storage.result_repository_protocol import ResultRepositoryProtocol

class GeometryResultRepository(ResultRepositoryProtocol[GeometryResult]):
    dsn: ClassVar[str | None] = None
    __srid: ClassVar[int | None] = None

    @classmethod
    def set_dsn(cls, dsn):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn


    @classmethod
    def set_geometry_srid(cls, srid: int):
        """Sets the SRID, so it can be explicitly specified for PostGIS geometry on database insertion.

        Args:
            srid (int): The EPSG code of the SRID. See for example: https://epsg.io/3035.
        """        
        cls.__srid = srid


    @classmethod
    def add(cls, validation_result: GeometryResult):
        """Adds a single GeometryResult to the repository.

        Args:
            validation_result (GeometryResult): The geometry result to be stored.
        """        
        cls.add_list([validation_result])


    @classmethod
    def add_list(cls, validation_results: list[GeometryResult]):
        """Adds multiple GeometryResults to the repository.

        Args:
            validation_results (list[GeometryResult]): The geometry results to be stored.
        """        
        if cls.dsn is None:
            raise Exception('Data Source Name (dsn) has not been set')
        if cls.__srid is None:
            raise Exception('SRID has not been set')

        
        commands = pydapper.connect(cls.dsn)
        insert_query_base = "INSERT INTO geometry_result " + \
                        "(run_id, validation_code, severity, feature_class, message, objectid, country, geometry, geometry_type) "
        insert_query = insert_query_base + \
                        "VALUES (?run_id?, ?validation_code?, ?severity?, ?feature_class?, ?message?, ?objectid?, ?country?, ST_Force2D(ST_SetSRID(?geometry?::geometry,?srid?)), ST_GeometryType(?geometry?))"
        insert_no_geom_query = insert_query_base + \
                        "VALUES (?run_id?, ?validation_code?, ?severity?, ?feature_class?, ?message?, ?objectid?, ?country?, NULL, NULL)"
        try:
            with commands:
                for geometry_result in validation_results:
                    if len(geometry_result.message) > 255:
                        geometry_result.message = geometry_result.message[:251] + "[..]"
                        print('*** WARNING: LOG MESSAGE TOO LONG', file=sys.stderr)

                    _ = commands.execute(
                        insert_no_geom_query if geometry_result.geometry is None else insert_query,
                        param = geometry_result.as_param_dict(cls.__srid)
                    )
        finally:
            commands.connection.close()


    @classmethod
    def get_by_run_id(cls, run_id: int) -> list[GeometryResult]:
        """Gets all GeometryResults for the validation-run with the given run_id.

        Args:
            run_id (int): The run id.

        Returns:
            list[GeometryResult]: All geometry results for the corresponding run.
        """        
        if cls.dsn is None:
            raise Exception('Data Source Name (dsn) has not been set')
        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                return commands.query(
                    "SELECT result_id, " +
					"       run_id, " +
					"		validation_code, " +
					"		severity, " +
					"		feature_class, " +
					"		message, " +
					"		objectid, " +
					"		ST_AsBinary(geometry) as geometry, " + # Converted to QgsGeometry in GeometryResult.from_query_row()
					"		geometry_type, " +
					"		country " +
                    "FROM geometry_result " + 
                    "WHERE run_id = ?run_id? " + 
                    "ORDER BY result_id ASC",
                    param = { "run_id": run_id},
                    model = GeometryResult.from_query_row)
        finally:
            commands.connection.close()


    @classmethod
    def get_by_vc_and_run_id(cls, validation_code: str, run_id: int) -> list[GeometryResult]:
        """Gets all GeometryResults for the given run_id and validation_code.

        Args:
            validation_code (str): The validation code.
            run_id (int): The run id.

        Returns:
            list[GeometryResult]: All geometry results for the corresponding run and validation code.
        """
        if cls.dsn is None:
            raise Exception('Data Source Name (dsn) has not been set')
        
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                return commands.query(
                    "SELECT result_id, " +
					"       run_id, " +
					"		validation_code, " +
					"		severity, " +
					"		feature_class, " +
					"		message, " +
					"		objectid, " +
					"		ST_AsBinary(geometry) as geometry, " + # Converted to QgsGeometry in GeometryResult.from_query_row()
					"		geometry_type " +
                    "FROM geometry_result " + 
                    "WHERE validation_code = ?validation_code? and run_id = ?run_id? " + 
                    "ORDER BY result_id ASC",
                    param = { "validation_code": validation_code, "run_id": run_id},
                    model = GeometryResult.from_query_row)
        finally:
            commands.connection.close()
