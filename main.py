import os
import sys
SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(SCRIPT_DIR)


from utilities import LogUtilities, QgisUtilities
from storage import StorageUtilities, ValidationLoggingRepository, ValidationTaskRepository, ValidationRunRepository, GeometryResultRepository, StatisticResultRepository, ValidationCheckStatusRepository
from models import ValidationTask, ValidationRun, ValidationParameters
from validators import *
import logging

import validation_specs # This import is required for collecting the data specifications
import vrailang

def main():
    (_, validation_params_json_filename) = tuple(sys.argv)

    params = ValidationParameters.from_json(validation_params_json_filename)
    if not params.are_complete():
        raise ValueError(f"Validation parameters are not complete. Check the parameters in {validation_params_json_filename}.")
    
    # Set srid
    SRID = "3035"
    # Set schemas
    AU_SCHEMA = "au"
    HY_SCHEMA = "hy"
    IB_SCHEMA = "ib"
    TN_SCHEMA = "tn"
    PUBLIC_SCHEMA = "public" # Use for test data only


    # Setup repositories
    StorageUtilities.setup_repositories(params.output_db_params.create_pg_dsn())
    GeometryResultRepository.set_geometry_srid(SRID)

    # Setup logging
    LogUtilities.configure_logging(level=LogUtilities.VERBOSE)
    logger = logging.getLogger(__name__)    
    logger.info("Setting up repositories")


    # Get task from database or create a new one if it doesn't exist yet
    logger.info("Setting up the current task")
    current_task = ValidationTaskRepository.get_by_task_name(params.task_name)
    if current_task is None:
        ValidationTaskRepository.add(ValidationTask(None, params.task_name))
        current_task = ValidationTaskRepository.get_by_task_name(params.task_name)

    # Create a new run
    logger.info("Setting up the current run")
    ValidationRunRepository.add(ValidationRun(None, current_task.task_id, params.to_json(), None, None, None))
    current_run = ValidationRunRepository.get_latest_by_task_id(current_task.task_id)
    # Add run_id to the logging
    ValidationLoggingRepository.set_current_run_id(current_run.run_id)

    try:              
        # Get QGIS info
        version = QgisUtilities.get_version()
        release_name = QgisUtilities.get_release_name()

        logger.info("")
        logger.info(f"{'Task name:':25} {params.task_name}")
        logger.info(f"{'Task id:':25} {current_task.task_id}")
        logger.info(f"{'Run id:':25} {current_run.run_id}")
        logger.info(f"{'QGIS Version:':25} {version}")
        logger.info(f"{'QGIS Release name:':25} {release_name}")
        logger.info(f"{'PG input host:':25} {params.input_db_params.host}")
        logger.info(f"{'PG input port:':25} {params.input_db_params.port}")
        logger.info(f"{'PG input database:':25} {params.input_db_params.name}")
        logger.info(f"{'PG input username:':25} {params.input_db_params.username}")
        logger.info(f"{'PG output DSN:':25} {params.output_db_params.create_pg_dsn()}")
        logger.info("")

        QgisUtilities.initialize_qgis()
        QgisUtilities.setup_postgis_connection(params.input_db_params.host, params.input_db_params.port, params.input_db_params.name, params.input_db_params.username, params.input_db_params.password)
        

        DataSchemaValidator.set_dsn(params.input_db_params.create_pg_dsn())
        CrsValidator.set_dsn(params.input_db_params.create_pg_dsn())
        
        # Retrieve the validation specs and start the validation
        validation_specs = vrailang.ValidationSpecification.ALL_SPECIFICATIONS[params.specification]
        validation_specs.run(current_run.run_id)


        # Create layers for QGIS

        # Test data
        #province_layer = QgisUtilities.create_postgres_vector_layer(PUBLIC_SCHEME, "provincies", "geom")
        #province_point_layer = QgisUtilities.create_postgres_vector_layer(PUBLIC_SCHEME, "provincie_punten", "geom")
        #topo_testdata_lijnen_layer = QgisUtilities.create_postgres_vector_layer(PUBLIC_SCHEME, "topo_testdata_lijnen", "geom")
        #topo_testdata_punten_layer = QgisUtilities.create_postgres_vector_layer(PUBLIC_SCHEME, "topo_testdata_punten", "geom")

        # OME2 data
        #administrative_unit_area_3_nl = QgisUtilities.create_postgres_vector_layer(AU_SCHEME, "administrative_unit_area_3", "geom", "country='nl'")


        # Parse field names and types
        # TODO move and use this in a validator which checks attribute data types
        #province_layer_fields = QgisUtilities.get_layer_fields(province_layer)

        # Run validations on test data
        # QueryValidator.run(current_run.run_id, "Q001", "WARNING", province_layer, '"Provincienaam" LIKE \'%-Holland\'')
        # MinimumAreaValidator.run(current_run.run_id, "M001", "WARNING", province_layer, minimum_area=2000000000)
        # ExtentValidator.run(current_run.run_id, "E001", "WARNING", province_layer, x_min=10000.000, y_min=306000.000, x_max=278000.000, y_max=622000.000)
        # MinimumVertexDistanceValidator.run(current_run.run_id, "M002", "WARNING", province_layer, minimum_distance=0.01)
        # CompletionRateValidator.run(current_run.run_id, "C001", "STATISTIC", province_layer, ["provincienaam", "test_tekst"])
        # MustBeSinglePartValidator.run(current_run.run_id, "M003", "ERROR", province_layer)
        # RegexValidator.run(current_run.run_id, "R001", "WARNING", province_layer, "provincienaam", "^N.*Holland$")
        # ValidGeometryValidator.run(current_run.run_id, "V001", "ERROR", province_layer)
        # AllowedAttributeValidator.run(current_run.run_id, "A001", "ERROR", province_layer, "type", ["provincie", "gemeente"])
        # PointAreaIdentifierConsistencyValidator.run(current_run.run_id, "P001", "ERROR", province_point_layer, province_layer, "provincienaam")
        # FeatureCountValidator.run(current_run.run_id, "F001", "STATISTIC", province_layer, minimum_record_count=20)

        # Run topology validations on test data
        # MustNotOverlapValidator.run(current_run.run_id, "M004", "ERROR", province_layer)
        # MustNotHaveGapsValidator.run(current_run.run_id, "M005", "ERROR", province_layer)
        # MustNotHaveDuplicatesValidator.run(current_run.run_id, "M006", "ERROR", province_layer)
        # MustNotHaveDanglesValidator.run(current_run.run_id, "M007", "ERROR", topo_testdata_lijnen_layer)
        # MustNotHavePseudosValidator.run(current_run.run_id, "M008", "ERROR", topo_testdata_lijnen_layer)
        # MustBeCoveredByValidator.run(current_run.run_id, "M009", "ERROR", province_point_layer, province_layer)
        # MustNotOverlapWithValidator.run(current_run.run_id, "M010", "ERROR", province_layer, province_layer)
        # MustBeCoveredByEndpointsOfValidator.run(current_run.run_id, "M011", "ERROR", topo_testdata_punten_layer, topo_testdata_lijnen_layer)
        # EndPointsMustBeCoveredByValidator.run(current_run.run_id, "M012", "ERROR", topo_testdata_lijnen_layer, topo_testdata_punten_layer)
        # MustBeInsideValidator.run(current_run.run_id, "M013", "ERROR", province_point_layer, province_layer)
        # MustContainValidator.run(current_run.run_id, "M014", "ERROR", province_layer, province_point_layer)

        # Run topology validations on OME2 data
        #MustNotHaveGapsValidator.run(current_run.run_id, "M005", "ERROR", administrative_unit_area_3_nl)

        # # OME2 data test merge
        # administrative_unit_area_3_nl = QgisUtilities.create_postgres_vector_layer(AU_SCHEMA, "administrative_unit_area_3", "geom", "country='nl'", layer_name="administrative_unit_area_3_NL")
        # administrative_unit_area_4_be = QgisUtilities.create_postgres_vector_layer(AU_SCHEMA, "administrative_unit_area_4", "geom", "country='be'", layer_name="administrative_unit_area_4_BE")
        # administrative_unit_area_4_fr = QgisUtilities.create_postgres_vector_layer(AU_SCHEMA, "administrative_unit_area_4", "geom", "country='fr'", layer_name="administrative_unit_area_4_FR")

        # administrative_units_merged = QgisUtilities.merge_vector_layers(
        #     [administrative_unit_area_3_nl, administrative_unit_area_4_be, administrative_unit_area_4_fr])
        

        # # Do some feature checks
        # MinimumAreaValidator.run(current_run.run_id, "M001", "WARNING", administrative_unit_area_3_nl, minimum_area=10000000)
        # MinimumVertexDistanceValidator.run(current_run.run_id, "M002", "WARNING", administrative_unit_area_3_nl, minimum_distance=0.01)
        
        # # Do some statistical checks
        # CompletionRateValidator.run(current_run.run_id, "C001", "STATISTIC", administrative_unit_area_3_nl, ["w_step"])
        # FeatureCountValidator.run(current_run.run_id, "F001", "STATISTIC", administrative_unit_area_3_nl, minimum_record_count=400)

        # # Check for gaps on merged layer
        # MustNotHaveGapsValidator.run(current_run.run_id, "M005", "ERROR", administrative_units_merged)
        # MustNotOverlapValidator.run(current_run.run_id, "M006", "ERROR", administrative_units_merged)

        # # Retrieve some results, turn them into vector layers and export to file on disk
        # M005_results = GeometryResultRepository.get_by_vc_and_run_id("M005", current_run.run_id)
        # M005_result_layers = GeometryResult.geometry_results_to_vector_layer_per_geom_type(M005_results, "M005_results" ,f"EPSG:{SRID}")
        
        # for _, layer in M005_result_layers:
        #     QgisUtilities.export_vector_layer(layer, 'GeoPackage')
        #     QgisUtilities.export_vector_layer(layer, 'ESRI Shapefile')
        #     QgisUtilities.export_vector_layer(layer, 'GeoJSON')
        #     QgisUtilities.export_vector_layer(layer, 'Geography Markup Language [GML]')
 
        
        # M001_results = GeometryResultRepository.get_by_vc_and_run_id("M001", current_run.run_id)
        # M001_result_layers = GeometryResult.geometry_results_to_vector_layer_per_geom_type(M001_results, "M001_results" ,f"EPSG:{SRID}")
        # for _, layer in M001_result_layers:
        #     QgisUtilities.export_vector_layer(layer, 'GeoPackage')


        #runway_line = QgisUtilities.create_postgres_vector_layer(TN_SCHEMA, "runway_line", "geom", "")
        #railway_line = QgisUtilities.create_postgres_vector_layer(TN_SCHEMA, "railway_line", "geom", "")

        #MinimumLengthValidator.run(current_run.run_id, "M101", "WARNING", runway_line, 1000)
        #MinimumLengthValidator.run(current_run.run_id, "M102", "WARNING", railway_line, 1000, check_multilines_per_linestring=True)
        #MinimumLengthValidator.run(current_run.run_id, "M103", "WARNING", [runway_line, railway_line], 1000)

        #road_service_area = QgisUtilities.create_postgres_vector_layer(TN_SCHEMA, "road_service_area", "geom", "")
        #NoAdjacentFacesSameAttributeValidator.run(current_run.run_id, "M201", "WARNING", road_service_area, ["type", "country"])
        #MinimumAreaValidator.run(current_run.run_id, "M202", "WARNING", road_service_area, 1000)

        #road_service_point = QgisUtilities.create_postgres_vector_layer(TN_SCHEMA, "road_service_point", "geom", "")

        #ProximityValidator.run(current_run.run_id, "M203", "WARNING", road_service_area, road_service_point, 50)

        # aerodrome_area = QgisUtilities.create_postgres_vector_layer(TN_SCHEMA, "aerodrome_area", "geom", "")
        #AttributeNotEmptyValidator.run(current_run.run_id, "A123", "WARNING", aerodrome_area, "country")
        #AttributeNotUnknownValidator.run(current_run.run_id, "A345", "WARNING", aerodrome_area, "designator_iata")


        # FeatureCountValidator.run(current_run.run_id, "F002", "STATISTIC", aerodrome_area)
        # FeatureCountValidator.run(current_run.run_id, "F003", "STATISTIC", aerodrome_area, 'country')
        # FeatureCountValidator.run(current_run.run_id, "F004", "STATISTIC", aerodrome_area, 'country', 'aerodrome_type')

        #road_link = QgisUtilities.create_postgres_vector_layer(TN_SCHEMA, "road_link", "geom", "")
        # AllowedAttributeValidator.run(current_run.run_id, "A001", "ERROR", road_link, "country", ['be', 'fr', 'gf', 'gp', 'mq', 'nl', 'pm', 're', 'yt'], separator='#')
        # AllowedAttributeValidator.run(current_run.run_id, "A002", "ERROR", road_link, "country", ['be', 'fr', 'gf', 'gp', 'nl', 'pm', 're', 'yt'])



        # administrative_unit_area_1 = QgisUtilities.create_postgres_vector_layer(AU_SCHEMA, "administrative_unit_area_1", "geom", "")
        # port_point = QgisUtilities.create_postgres_vector_layer(TN_SCHEMA, "port_point", "geom", "")
        # runway_line = QgisUtilities.create_postgres_vector_layer(TN_SCHEMA, "runway_line", "geom", "")
        # road_service_area = QgisUtilities.create_postgres_vector_layer(TN_SCHEMA, "road_service_area", "geom", "")

        # FeatureAreaIdentifierConsistencyValidator.run(current_run.run_id, "F001", "ERROR", port_point, administrative_unit_area_1, "country")
        # FeatureAreaIdentifierConsistencyValidator.run(current_run.run_id, "F002", "ERROR", runway_line, administrative_unit_area_1, "country")
        # FeatureAreaIdentifierConsistencyValidator.run(current_run.run_id, "F003", "ERROR", road_service_area, administrative_unit_area_1, "country")


        # GeometryTypeValidator.run(current_run.run_id, "G008", "ERROR", port_point, expected_geometry_type=QgsWkbTypes.PointZ)
        # GeometryTypeValidator.run(current_run.run_id, "G009", "ERROR", administrative_unit_area_1, expected_geometry_type=QgsWkbTypes.MultiPolygon)
        # GeometryTypeValidator.run(current_run.run_id, "G010", "ERROR", port_point, expected_geometry_type=QgsWkbTypes.MultiPointZ)

        #CrsValidator.run(current_run.run_id, "C001", "ERROR", port_point, epsg_code=3035, schema=TN_SCHEMA)

        # port_point_attributes = {
        #     'objectid': 'uuid',
        #     'country': 'character varying',
        #     'begin_lifespan_version': 'timestamp without time zone',
        #     'end_lifespan_version': 'timestamp without time zone',
        #     'geom': 'USER-DEFINED',
        #     'name': 'jsonb',
        #     'label': 'character varying',
        #     'un_locode': 'character varying',
        #     'tent_network': 'character varying',
        #     'w_national_identifier': 'character varying',
        #     'w_step': 'integer',
        #     'xy_source': 'character varying',
        #     'z_source': 'character varying',
        #     #'w_scale': 'character varying',
        #     'w_scale': 'jsonb', # for test purposes only
        #     'wwww_release': 'integer' # for test purposes only, should be 'w_release'
        # }
        #DataSchemaValidator.run(current_run.run_id, "D009", "STATISTIC", port_point, expected_attribute_types=port_point_attributes, schema=TN_SCHEMA) # TODO Enable ERROR severiry and rename result type?


        logger.info("")
        geom_results = GeometryResultRepository.get_by_run_id(current_run.run_id)
        logger.info(f"{'Number of geometry results:':35} {len(geom_results)}")
        stat_results = StatisticResultRepository.get_by_run_id(current_run.run_id)
        logger.info(f"{'Number of statistic results:':35} {len(stat_results)}")
        all_checks = ValidationCheckStatusRepository.get_checks_by_run_id(current_run.run_id)
        logger.info(f"{'Number of total checks:':35} {len(all_checks)}")
        failed_checks = ValidationCheckStatusRepository.get_checks_by_run_id(current_run.run_id, failed_only=True)
        logger.info(f"{'Number of failed checks:':35} {len(failed_checks)}")
        logger.info("")


    finally:
        ValidationRunRepository.update_on_end(current_run)
        QgisUtilities.exit_qgis()
        

if __name__ == "__main__":
    main()
