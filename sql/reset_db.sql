TRUNCATE TABLE validation_task CASCADE;
TRUNCATE TABLE validation_run CASCADE;
TRUNCATE TABLE validation_logging CASCADE;
TRUNCATE TABLE geometry_result CASCADE;
TRUNCATE TABLE generic_result CASCADE;
TRUNCATE TABLE validation_check_status CASCADE;

ALTER SEQUENCE validation_logging_log_id_seq RESTART WITH 1;
ALTER SEQUENCE geometry_result_result_id_seq RESTART WITH 1;
ALTER SEQUENCE generic_result_result_id_seq RESTART WITH 1;
ALTER SEQUENCE validation_run_run_id_seq RESTART WITH 1;
ALTER SEQUENCE validation_task_task_id_seq RESTART WITH 1;
