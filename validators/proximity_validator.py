from qgis.core import QgsSpatialIndex, QgsVectorLayer
from qgis import processing
import logging
from models import ValidationResult
from . import FeatureValidator
from utilities import QgisUtilities
from qgis.PyQt.QtCore import QMetaType
from typing import Union

class ProximityValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class_1: QgsVectorLayer, feature_class_2: QgsVectorLayer, distance: Union[int, float] ) -> list[ValidationResult]:
        """Runs the ProximityValidator.

        Selects objects in featureaclass 2 which are not within a certain distance of featureclass 1.
        TODO The ERM Validator has the option to invert this validation (WithinDistance = True/False).

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class_1 (QgsVectorLayer): The featureclass which is used for the proximity comparison.
            feature_class_2 (QgsVectorLayer): The featureclass of which the features are checked for proximity.
            distance (Union[int, float]): The distance in meters.

        Returns:
            list[ValidationResult]: A list of results, containing the features of featureclass 2 which are not within a certain distance of feeatures in featureclass 1.
        """        
        results = []

        if type(distance) not in [int, float] or distance < 0:
            log_message = f"Skipping {cls.__name__} on '{feature_class_2.name()}' since the proximity distance is not an int or float larger than 0."
            cls.logger.warning(log_message)
            return results
        
        # QGIS cannot buffer layers with PostgreSQL datatype jsonb, such as 'name'
        # Therefore we prepare layers by skipping certain fields
        feature_class_1_prepared = QgisUtilities.create_memory_layer(feature_class_1, skip_field_types = [QMetaType.QVariantMap])
        
        # Create a dissolved buffer around featureclass1
        buffer_layer = "memory:buffer_layer"
        buffer_parameters = {
            'INPUT':feature_class_1_prepared,
            'DISTANCE':distance,
            'SEGMENTS':5,
            'END_CAP_STYLE':0,
            'JOIN_STYLE':0,
            'MITER_LIMIT':2,
            'DISSOLVE':False , # DISSOLVE = True could be used, but large multipolygons seem to have a very bad effect on performance
            'OUTPUT':buffer_layer
        }

        cls.logger.info(f"Start creating buffer ...")
        buffer = processing.run("native:buffer", buffer_parameters) # Run processing.algorithmHelp("native:buffer") for documentation
        buffer_layer = buffer['OUTPUT']
        cls.logger.info(f"Finished creating buffer.")

        
        index = QgsSpatialIndex(buffer_layer.getFeatures(), flags=QgsSpatialIndex.FlagStoreFeatureGeometries)

        for feature in feature_class_2.getFeatures():
            g1 = feature.geometry()
            bb = g1.boundingBox()
            candidate_ids = index.intersects( bb )

            intersects = False
            for candidate_id in candidate_ids:

                # Retrieve geometry via index
                g2 = index.geometry(candidate_id)

                # Check for valid geometry
                if QgisUtilities.is_empty_or_invalid_geometry(g2):
                    continue

                # A single intersect means that the feature is within proximity
                if feature.geometry().intersects(g2):
                    intersects = True
                    break

            if not intersects:
                # Create results
                message = f"{feature_class_2.name()} feature with objectid '{feature['objectid']}' is not within {distance} meters of {feature_class_1.name()}."
                result = cls.create_result(run_id, validation_code, severity, feature_class_2, feature, message)
                results.append(result)

        return results
