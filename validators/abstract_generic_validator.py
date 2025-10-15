from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QVariant
from abc import ABC
from . import AbstractValidator
from models import GenericResult
from storage import GenericResultRepository

class GenericValidator(AbstractValidator, ABC):
    result_repository = GenericResultRepository
    
    @classmethod
    def create_result(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, message: str, country: str | None = None) -> GenericResult:
        """Creates a GenericResult.

        Creates a GenericResult which can be stored in the GenericResultRepository.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class.
            message (str): A description of the generic result.
            country (str | None): Country code of the feature (optional).

        Returns:
            GenericResult: A generic result ready for database insertion.
        """

        # Typed nulls for satisfying the typechecker
        GENERATE_ID: int = None  # type: ignore

        return GenericResult(
            result_id = GENERATE_ID,
            run_id = run_id,
            validation_code = validation_code,
            severity  = severity,
            feature_class = feature_class.name(),
            message = message,
            country = country
        )

    @classmethod
    def create_field_doesnt_exist_message(cls, feature_class: QgsVectorLayer, field_name: str) -> str:
        """Creates a message indicating the validator will skip validations for a feature class because a field does not exist.

        Args:
            feature_class (QgsVectorLayer): The feature class with the missing field.
            field_name (str): The name of the field that is missing.

        Returns:
            str: The skip message.
        """
        return f"Skipping {cls.__name__} on '{feature_class.name()}' for field {field_name} because the field does not exist."


    @classmethod
    def get_equals_expression(cls, field_name: str, value: str | QVariant) -> str:
        """Creates an equality expression that can be passed as an argument to `QgsVectorLayer.selectByExpression`.

        Args:
            field_name (str): The name of the field.
            value (str | QVariant): The value the field should equal to.

        Returns:
            str: The equality expression.
        """
        if type(value) is QVariant and value.isNull():
            return f'"{field_name}" is {value}'
        return f'"{field_name}" = \'{value}\''
    
    @classmethod
    def get_unique_values(cls, feature_class: QgsVectorLayer, field_name: str) -> list[str]:
        """Gets a list of all values used for a feature class's field.

        Args:
            feature_class (QgsVectorLayer): The feature class.
            field_name (str): The name of the field.

        Returns:
            list[str]: The values that are in use for the feature class's field.
        """
        field_index = feature_class.fields().indexFromName(field_name) 
        return sorted(feature_class.uniqueValues(field_index))
