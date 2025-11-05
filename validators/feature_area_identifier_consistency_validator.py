from typing import Any
from qgis.core import QgsVectorLayer
from qgis import processing
from models import ValidationResult
from . import FeatureValidator

from processing.tools import *
import logging

from utilities import QgisUtilities
from qgis.PyQt.QtCore import QMetaType


class FeatureAreaIdentifierConsistencyValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, check_feature_class: QgsVectorLayer, area_feature_class: QgsVectorLayer, id_field: str,
                 attribute_mapping: dict[Any,Any] | None = None) -> list[ValidationResult]:
        """Runs the FeatureAreaIdentifierConsistencyValidator.
        
        Checks if every feature from the check-featureclass is inside an area of the area-featureclass while also having matching values for the id field.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            check_feature_class (QgsVectorLayer): The featureclass containing the objects to check.
            area_feature_class (QgsVectorLayer): The featureclass containing areas.
            id_field (str): The corresponding ID field linking the check and area featureclasses.
            attribute_mapping (dict[Any,Any] | None): Optional mapping that 
                translates values of the ID field in check_feature_class to values that are used in area_feature_class.

        Returns:
            list[ValidationResult]: A list of results, containing the check features which are either not inside an area or do not having a matching id field value.
        """      
        results = []

        # Remove fields of type jsonb to enable processing with QGIS algorithms
        prepared_check_feature_class = QgisUtilities.create_memory_layer(check_feature_class, skip_field_types = [QMetaType.QVariantMap])
        prepared_area_feature_class = QgisUtilities.create_memory_layer(area_feature_class, skip_field_types = [QMetaType.QVariantMap])

        join_layer = "memory:join_layer"
        parameters = {
        'INPUT':prepared_check_feature_class,
        'PREDICATE':[5], # WITHIN
        'JOIN': prepared_area_feature_class,
        'JOIN_FIELDS':[],
        'METHOD':0,
        'DISCARD_NONMATCHING':False,
        'PREFIX':'',
        'OUTPUT':join_layer}

        join_by_location = processing.run("native:joinattributesbylocation", parameters) # Run processing.algorithmHelp("native:joinattributesbylocation") for documentation
        join_by_location_layer = join_by_location['OUTPUT']

        for feature in join_by_location_layer.getFeatures():
            feature_objectid = feature.attribute('objectid')
            feature_id_value = feature.attribute(id_field)
            area_objectid = feature.attribute('objectid_2')
            area_id_value = feature.attribute(f'{id_field}_2')

            # Translate feature ID value to value used for comparison
            feature_id_value_cmp = (
                attribute_mapping.get(feature_id_value, feature_id_value) 
                if attribute_mapping 
                else feature_id_value
            )
            
            # Feature is not contained by Area
            if area_id_value is None:
                message = f"{check_feature_class.name()} feature with objectid \'{feature_objectid}\' and {id_field} = \'{feature_id_value}\' is not within any {area_feature_class.name()} feature."
                country = country = cls.get_attribute(feature, 'country')
                result = cls.create_result(
                    run_id,
                    validation_code,
                    severity,
                    check_feature_class,
                    feature,
                    message,
                    country
                )
                results.append(result)

            # Feature is in Area but the id_field's do not match
            elif feature_id_value_cmp != area_id_value:
                message = f"{check_feature_class.name()} feature with objectid \'{feature_objectid}\' and {id_field} = \'{feature_id_value}\' mismatches {area_feature_class.name()} feature with objectid \'{area_objectid}\' and {id_field} = \'{area_id_value}\'."
                country = cls.get_attribute(feature, 'country')
                result = cls.create_result(
                    run_id,
                    validation_code,
                    severity,
                    check_feature_class,
                    feature,
                    message,
                    country
                )
                results.append(result)

        return results
