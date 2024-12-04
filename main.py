import os
import sys
SCRIPT_DIR = os.path.dirname(__file__)
sys.path.append(SCRIPT_DIR)


from utilities import LogUtilities, QgisUtilities
from storage import StorageUtilities, ValidationLoggingRepository, ValidationTaskRepository, ValidationRunRepository, GeometryResultRepository, GenericResultRepository, ValidationCheckStatusRepository
from models import ValidationTask, ValidationRun, ValidationParameters
from validators import *
import logging

import validation_specs # noqa: F401  # This import is required for collecting the data specifications
import vrailang

def main():
    (_, validation_params_json_filename) = tuple(sys.argv)

    params = ValidationParameters.from_json(validation_params_json_filename)
    if not params.are_complete():
        raise ValueError(f"Validation parameters are not complete. Check the parameters in {validation_params_json_filename}.")
    
    # Set srid
    SRID = "3035"

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

    params.task_id = current_task.task_id
    params.run_id = current_run.run_id

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
        UniqueFieldValidator.set_dsn(params.input_db_params.create_pg_dsn())
        
        # Retrieve the validation specification and start the validation
        validation_specs = vrailang.ValidationSpecification.ALL_SPECIFICATIONS[params.specification]
        validation_specs.run(params, arg_loader)

        logger.info("")
        geom_results = GeometryResultRepository.get_by_run_id(current_run.run_id)
        logger.info(f"{'Number of geometry results:':35} {len(geom_results)}")
        generic_results = GenericResultRepository.get_by_run_id(current_run.run_id)
        logger.info(f"{'Number of generic results:':35} {len(generic_results)}")
        all_checks = ValidationCheckStatusRepository.get_checks_by_run_id(current_run.run_id)
        logger.info(f"{'Number of total checks:':35} {len(all_checks)}")
        failed_checks = ValidationCheckStatusRepository.get_checks_by_run_id(current_run.run_id, failed_only=True)
        logger.info(f"{'Number of failed checks:':35} {len(failed_checks)}")
        logger.info("")


    finally:
        ValidationRunRepository.update_on_end(current_run)
        QgisUtilities.exit_qgis()


def arg_loader(arg: object) -> object:
    # We can't seem to do type checking during runtime on 'feature' or 'FeatureMetaclass' in rules.py due to circular dependencies.
    if vrailang.isfeatureclass(arg):
        return QgisUtilities.create_postgres_vector_layer(arg.THEME.schema, arg.__name__, "geom")
    return arg


if __name__ == "__main__":
    main()
