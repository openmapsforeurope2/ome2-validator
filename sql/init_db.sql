--
-- Create table for Validation task
-- 
CREATE TABLE validation_task (
  task_id SERIAL PRIMARY KEY,
  name VARCHAR (255) UNIQUE NOT NULL
);

COMMENT ON TABLE validation_task IS 'Table for storing validation tasks.';

CREATE INDEX idx_validation_task_id ON validation_task(task_id);


--
-- Create table for validation run
-- 
CREATE TABLE validation_run (
  run_id SERIAL PRIMARY KEY,
  task_id INT,
  parameters JSON,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  in_progress BOOLEAN,
  CONSTRAINT fk_task
      FOREIGN KEY(task_id) 
        REFERENCES validation_task(task_id)
);

COMMENT ON TABLE validation_run IS 'Table for storing validation runs.';

CREATE INDEX idx_validation_run_id ON validation_run(run_id);


--
-- Create table for logging
-- 
CREATE TABLE validation_logging (
  log_id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL,
  run_id INT,
  severity VARCHAR (7) NOT NULL CHECK (severity IN ('VERBOSE', 'DEBUG', 'INFO', 'WARNING', 'ERROR')),
  message VARCHAR (255) NOT NULL,
  module VARCHAR (255) NOT NULL
);

COMMENT ON TABLE validation_logging IS 'Table for storing the logging.';

CREATE INDEX idx_validation_logging_run_id ON validation_logging(run_id);


--
-- Create table for geometry results
-- 
CREATE TABLE geometry_result (
  result_id SERIAL PRIMARY KEY,
  run_id INT,
  validation_code VARCHAR (4),
  severity VARCHAR (9) NOT NULL CHECK (severity IN ('WARNING', 'ERROR')),
  feature_class VARCHAR (255),
  message VARCHAR (255),
  objectid uuid,
  geometry geometry(Geometry,3035),
  geometry_type VARCHAR (255),
  CONSTRAINT fk_run
    FOREIGN KEY(run_id) 
      REFERENCES validation_run(run_id)
);

COMMENT ON TABLE geometry_result IS 'Table for storing the geometry results for a validation.';

CREATE INDEX idx_geometry_result_id ON geometry_result(result_id);

--
-- Create table for statistic results
-- 
CREATE TABLE statistic_result (
  result_id SERIAL PRIMARY KEY,
  run_id INT,
  validation_code VARCHAR (4),
  severity VARCHAR (9) NOT NULL CHECK (severity IN ('WARNING', 'ERROR', 'STATISTIC')),
  feature_class VARCHAR (255),
  message VARCHAR (255),
  CONSTRAINT fk_run
    FOREIGN KEY(run_id) 
      REFERENCES validation_run(run_id)
);

COMMENT ON TABLE statistic_result IS 'Table for storing the statistic results for a validation.';

CREATE INDEX idx_statistic_result_id ON statistic_result(result_id);


--
-- Create table for validation check status
-- 
CREATE TABLE validation_check_status (
  validation_code VARCHAR(4) NOT NULL,
  run_id INT NOT NULL,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  last_update TIMESTAMP,
  success BOOLEAN,
  UNIQUE (validation_code, run_id),
  CONSTRAINT fk_run
    FOREIGN KEY(run_id) 
      REFERENCES validation_run(run_id)
);

COMMENT ON TABLE validation_check_status IS 'Table for storing the validation check statusses.';

CREATE INDEX idx_validation_check_status_run_id ON validation_check_status(run_id);


--
-- Create settings table, including the current version
--
DROP TABLE IF EXISTS validation_settings;
CREATE TABLE validation_settings (
  setting VARCHAR(30) NOT NULL UNIQUE,
  value VARCHAR(200)
);

COMMENT ON TABLE validation_settings IS 'Table for storing settings.';

INSERT INTO validation_settings values ('version', '0.1');
