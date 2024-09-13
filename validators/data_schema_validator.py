from qgis.core import QgsVectorLayer
from models import ValidationResult
from . import GenericValidator
import logging
import pydapper
from dataclasses import dataclass

class DataSchemaValidator(GenericValidator):
    logger = logging.getLogger(__name__)
    dsn = None

    
    @dataclass
    class TableExistsQueryRecord:
        exists: bool

    
    @dataclass
    class AttributeTypeRecord:
        column_name: str
        data_type: str
        length: int


    @classmethod
    def set_dsn(cls, dsn):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, expected_attribute_types: dict, schema: str) -> list[ValidationResult]:
        """Runs the DataSchemaValidator.
        """
        results = []

        # Check if the source-table exists in Postgres
        table_exists_record = None
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                table_exists_record = commands.query_first(
                    f"SELECT EXISTS( \
                        SELECT 1 \
                        FROM information_schema.tables \
                        WHERE table_schema = '{schema}' \
                        AND table_name = '{feature_class.name()}' \
                    );",
                model = cls.TableExistsQueryRecord
                )
        finally:
            commands.connection.close()

        if not table_exists_record.exists:
            message = f"Featureclass '{feature_class.name()}' does not exist in the database, but should exist according to the dataschema."
            result = cls.create_result(run_id, validation_code, severity, feature_class, message)
            results.append(result)
            return results
        
        column_records = []
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                column_records = commands.query(
                    f"SELECT column_name, udt_name as data_type, character_maximum_length as length \
                      FROM information_schema.columns \
                      WHERE table_schema = '{schema}' \
                      AND table_name = '{feature_class.name()}' \
                      ORDER BY ordinal_position ASC;",
                      model = cls.AttributeTypeRecord
                )
             
        finally:
            commands.connection.close()

        # Find and report missing and additional columns
        expected_column_names = set([key for key in expected_attribute_types.keys()])
        actual_column_names = set([record.column_name for record in column_records])

        missing_column_names = list(sorted(expected_column_names - actual_column_names))
        added_column_names = list(sorted(actual_column_names - expected_column_names))
        
        for missing_column_name in missing_column_names:
            message = f"Featureclass '{feature_class.name()}' is missing a column named '{missing_column_name}', which should exist according to the dataschema."
            result = cls.create_result(run_id, validation_code, severity, feature_class, message)
            results.append(result)

        for added_column_name in added_column_names:
            message = f"Featureclass '{feature_class.name()}' has a column named '{added_column_name}', which should not exist according to the dataschema."
            result = cls.create_result(run_id, validation_code, severity, feature_class, message)
            results.append(result)

        # Find and report mismatches in datatype and length
        for column in [column for column in column_records if column.column_name not in added_column_names]:
            expected_column_type, expected_column_length = expected_attribute_types[column.column_name]
            if expected_column_type != column.data_type:
                message = f"Featureclass '{feature_class.name()}' has a column named '{column.column_name}' of type '{column.data_type}', which should be of type '{expected_column_type}' according to the dataschema."
                result = cls.create_result(run_id, validation_code, severity, feature_class, message)
                results.append(result)

            if expected_column_length is not None and expected_column_length != column.length:
                message = f"Featureclass '{feature_class.name()}' has a column named '{column.column_name}' of length '{column.length}', which should be of length '{expected_column_length}' according to the dataschema."
                result = cls.create_result(run_id, validation_code, severity, feature_class, message)
                results.append(result)

        return results
