
from dataclasses import dataclass
from typing import ClassVar
from qgis.core import QgsVectorLayer
from models import ValidationResult
from . import GenericValidator
from utilities import QgisUtilities
import logging
import pydapper

class UniqueFieldValidator(GenericValidator):
    logger: ClassVar[logging.Logger] = logging.getLogger(__name__)
    dsn: ClassVar[str | None] = None

    @classmethod
    def set_dsn(cls, dsn):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn


    @dataclass
    class IsUniqueRecord:
        is_unique: bool

    @dataclass
    class NonUniqueCountRecord:
        value: str
        count: int


    
    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, fieldname: str, schema: str) -> list[ValidationResult]:
        if cls.dsn is None:
            raise Exception('Data Source Name (dsn) has not been set')
        
        results = []

        if not QgisUtilities.layer_has_field(feature_class, fieldname):
            cls.logger.warning(f"Cannot run the {cls.__name__} on {feature_class.name()} for field {fieldname} because the field does not exist.")
            return results

        is_unique_record = None
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                is_unique_record = commands.query_single(
                    f"SELECT COUNT(DISTINCT {fieldname}) = COUNT(*) AS is_unique \
                        FROM {schema}.{feature_class.name()}",
                model = cls.IsUniqueRecord
                )

        finally:
            commands.connection.close()

        if (is_unique_record.is_unique):
            return results
        
        non_unique_count_records = None
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                non_unique_count_records = commands.query(
                    f"SELECT {fieldname} value, COUNT(*) count \
                        FROM {schema}.{feature_class.name()} \
                        GROUP BY({fieldname}) HAVING COUNT(*) > 1;",
                    model = cls.NonUniqueCountRecord
                )

        finally:
            commands.connection.close()

        for record in non_unique_count_records:
            message = f"Featureclass '{feature_class.name()}' contains {record.count} features with value '{record.value}' for unique field '{fieldname}'."
            country = None # TODO: Implement per country statistics?
            result = cls.create_result(
                run_id,
                validation_code,
                severity,
                feature_class,
                message,
                country
            )
            results.append(result)

        return results
