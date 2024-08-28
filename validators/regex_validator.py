from qgis.core import QgsFeatureRequest, QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
import re
import logging

class RegexValidator(FeatureValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, field_name: str, regex: str) -> list[ValidationResult]:
        """Runs the RegexValidator.

        Checks if the specified field value complies with a regular expression.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            field_name (str): The field on which the regular expression is used.
            regex (str): The regular expression.

        Returns:
            list[ValidationResult]: A list of results, containing the features of which the specified field value does not match the given regex.
        """        
        results = []

        # TODO Using the regex in the filter expression will probably have better performance, but regex is not parsed correctly
        #filter_regex = f"regexp_match(\"{field_name}\", {regex})"
        #for feature in feature_class.getFeatures(QgsFeatureRequest().setFilterExpression(filter_regex)):

        # Check if the field exists in the layer
        field_index = feature_class.fields().indexFromName(field_name)
        if field_index == -1:
            cls.logger.error(f"FeatureClass {feature_class} does not have field {field_name}")
            return

        pattern = re.compile(regex)

        for feature in feature_class.getFeatures():
            value = feature.attribute(field_name)

            if pattern.match(value) is None:
                message = f'RegexValidator result for regex: {regex}'
                result = cls.create_result(run_id, validation_code, severity, feature_class, feature, message)
                results.append(result)

        return results
