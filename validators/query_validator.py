from qgis.core import QgsFeatureRequest, QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
import logging

class QueryValidator(FeatureValidator):
    logger = logging.getLogger(__name__)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, where_clause: str) -> list[ValidationResult]:
        """Runs the QueryValidator.

        Selects objects in a given feature class based on a where-clause.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
            where_clause (str): The where-clause.

        Returns:
            list[ValidationResult]: A list of results, containing the features which were selected by the where-clause.
        """        
        results = []

        for feature in feature_class.getFeatures(QgsFeatureRequest().setFilterExpression(where_clause)):
            message = f'QueryValidator result for query: {where_clause}'
            result = cls.create_result(
                run_id,
                validation_code,
                severity,
                feature_class,
                feature,
                message,
                cls.get_attribute(feature, 'country') 
            )
            results.append(result)

        return results
