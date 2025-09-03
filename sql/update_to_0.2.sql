-- Migrate from 0.1 (init) to 0.2

ALTER TABLE generic_result
   ADD COLUMN country VARCHAR(8) DEFAULT NULL;

ALTER TABLE geometry_result
   ADD COLUMN country VARCHAR(8) DEFAULT NULL;

CREATE OR REPLACE VIEW geometry_result_null AS
  SELECT 
    result_id, 
    run_id, 
    validation_code, 
    severity, 
    feature_class, 
    message, 
    objectid,
    ST_GeomFromText('POINT(0 0)'),
    country
  FROM geometry_result
  WHERE geometry IS NULL;

UPDATE validation_settings SET value = '0.2' WHERE setting = 'version';
