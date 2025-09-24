from PyQt5.QtCore import QVariant
from qgis.core import QgsVectorLayer
from models import ValidationResult
from . import GenericValidator
from utilities import QgisUtilities
import logging

class CompletionRateValidator(GenericValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, field_names: list[str]) -> list[ValidationResult]:
        """Runs the CompletionRateValidator.

        The percentage of NULL, 'void_unk' or empty string (i.e. '  ') values is calculated for each specified field in the given featureclass.
        When this percentage is higher than 0 a corresponding validation results is created.

        TODO OME2 data contains 'void_unk' for unknown values while ERM data contains 'UNK'.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            field_names (list[str]): A list of field names.

        Returns:
            list[ValidationResult]: A list of results, containing the percentage of NULL, 'void_unk' and/or empty string values per field.
        """        
        results = []

        # Check field existence
        for field_name in field_names:
            if not QgisUtilities.layer_has_field(feature_class, field_name):
                cls.logger.warning(f"Cannot run the {cls.__name__} on {feature_class.name()} for field {field_name} because the field does not exist.")
                return results

        # Get total feature count
        total_records = feature_class.featureCount()

        if total_records == 0:
            return results
        
        for field_name in field_names:
            null_records = 0
            unknown_records = 0
            empty_string_records = 0

            for feature in feature_class.getFeatures():
                value = feature.attribute(field_name)

                # Check for NULL values
                if isinstance(value, QVariant) and value.isNull():
                    null_records += 1
                
                # Check for Unknown values
                if value == 'void_unk':
                    unknown_records += 1

                # Check for empty string values
                if isinstance(value, str) and value.strip() == '':
                    empty_string_records += 1

            # Write results
            result_types = [
                ("NULL", null_records),
                ("'void_unk'", unknown_records),
                ("empty string", empty_string_records)
            ]

            for result_type in result_types:
                name, records = result_type
                perc = round(records * 100.0 / total_records, 1)
                
                message = f"Featureclass '{feature_class.name()}' field '{field_name}' has {perc}% {name} values ({records} out of {total_records})"
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
