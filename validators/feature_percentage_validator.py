from typing import Any

from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QVariant
from models import ValidationResult
from . import GenericValidator
from utilities import QgisUtilities
import logging


class FeaturePercentageValidator(GenericValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, value: str,
                 group_by_field_2: str, group_by_field_1: str | None = None) -> list[ValidationResult]:
        """Runs the FeaturePercentageValidator

        Calculates the percentage of features that have a certain value for a field.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            group_by_field_1 (str): A group by field. Defaults to None.
            group_by_field_2 (str): A second group by field.
            value (str): The value group_by_field_2 should have.

        Returns:
            list[ValidationResult]: A list of 0 or 1 results, describing the feature count for this featureclass.
        """
        results = []

        if group_by_field_1 and not QgisUtilities.layer_has_field(feature_class, group_by_field_1):
            cls.logger.warning(cls.create_field_doesnt_exist_message(feature_class, group_by_field_1))
            return results

        if group_by_field_2 and not QgisUtilities.layer_has_field(feature_class, group_by_field_2):
            cls.logger.warning(cls.create_field_doesnt_exist_message(feature_class, group_by_field_2))
            return results

        if group_by_field_1 and not group_by_field_2:
            log_message = f"Skipping {cls.__name__} on '{feature_class.name()}' since a second groupby-field cannot be used without a first groupby-field."
            cls.logger.warning(log_message)
            return results

        expressions_1 = []
        expressions_2 = []

        if group_by_field_1:
            for val_1 in cls.get_unique_values(feature_class, group_by_field_1):
                exp1 = cls.get_equals_expression(group_by_field_1, val_1)
                exp2 = cls.get_equals_expression(group_by_field_2, value)
                expressions_1.append(exp1)
                expressions_2.append(f'{exp1} AND {exp2}')
        else:
            exp2 = cls.get_equals_expression(group_by_field_2, value)
            expressions_2.append(exp2)

        if not expressions_1:
            feature_count1 = feature_class.featureCount()
            feature_class.selectByExpression(expressions_2[0])
            feature_count2 = feature_class.selectedFeatureCount()
            feature_class.removeSelection()
            perc = round((feature_count2 / feature_count1) * 100, 1)
            message = f"Featureclass '{feature_class.name()}' field '{group_by_field_2}' has {perc}% {value} values ({feature_count2} out of {feature_count1})"
            result = cls.create_result(run_id, validation_code, severity, feature_class, message)
            results.append(result)

        else:
            for i in range(len(expressions_1)):
                feature_class.selectByExpression(expressions_1[i])
                feature_count1 = feature_class.selectedFeatureCount()
                feature_class.removeSelection()
                feature_class.selectByExpression(expressions_2[i])
                feature_count2 = feature_class.selectedFeatureCount()
                feature_class.removeSelection()
                perc = round((feature_count2 / feature_count1) * 100, 1)
                message = f"For featureclass '{feature_class.name()}' and {expressions_1[i]}, field '{group_by_field_2}' has {perc}% {value} values ({feature_count2} out of {feature_count1})"
                result = cls.create_result(run_id, validation_code, severity, feature_class, message)
                results.append(result)

        return results

    @classmethod
    def create_field_doesnt_exist_message(cls, feature_class, group_by_field) -> str:
        return f"Skipping {cls.__name__} on '{feature_class.name()}' for field {group_by_field} because the field does not exist."

    @classmethod
    def get_equals_expression(cls, field, value) -> str:
        if type(value) is QVariant and value.isNull():
            return f'"{field}" is {value}'
        return f'"{field}" = \'{value}\''

    @classmethod
    def get_unique_values(cls, feature_class, field_name) -> list[str]:
        field_index = feature_class.fields().indexFromName(field_name)
        return sorted(feature_class.uniqueValues(field_index))
