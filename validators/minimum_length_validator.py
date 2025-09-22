from qgis.core import QgsWkbTypes, QgsVectorLayer
from models import ValidationResult
from . import FeatureValidator
import logging
from utilities import QgisUtilities
from typing import Union

class MinimumLengthValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_classes: Union[QgsVectorLayer, list[QgsVectorLayer]], minimum_length: Union[int, float], check_multilines_per_linestring: bool = False) -> list[ValidationResult]:
        """Runs the MinimumLengthValidator.

        Checks if polygon features in the given featureclass are shorter than the minimum length.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_classes (Union[QgsVectorLayer, list[QgsVectorLayer]]): One or more featureclasses to check. Must contain line-geometry.
            minimum_length (Union[int, float]): The minimum length of line features.
            check_multilines_per_linestring (bool, optional): Option to check individual line_parts for a multilinestring. Defaults to False.

        Returns:
            list[ValidationResult]: A list of results, containing the features which are shorter than the minimum distance.
        """        
        results = []

        # Parameter may be an array of QgsVectorLayers or a single one
        if type(feature_classes) is QgsVectorLayer:
            feature_classes = [feature_classes]

        if type(minimum_length) not in [int, float] or minimum_length < 0:
            log_message = f"Skipping {cls.__name__} on '{tuple(f.name() for f in feature_classes)}' since the minimum_length is not an int or float larger than 0."
            cls.logger.warning(log_message)
            return results

        # Using a request filter improves performance, however this does not easily allow for separate handling of linestrings of a multiline
        # request = QgsFeatureRequest(QgsExpression(f'$length < {minimum_length}'))
        
        for feature_class in feature_classes:

            # Check geometry type
            if feature_class.geometryType() != QgsWkbTypes.GeometryType.LineGeometry:
                log_message = cls.get_invalid_geometry_type_message(feature_class, [QgsWkbTypes.GeometryType.LineGeometry])
                cls.logger.warning(log_message)
                continue

            #for feature in feature_class.getFeatures(request):
            for feature in feature_class.getFeatures():

                # Check for valid geometry
                if QgisUtilities.is_empty_or_invalid_geometry(feature.geometry()):
                    log_message = cls.get_empty_or_invalid_geometry_message(feature_class, feature)
                    cls.logger.warning(log_message)
                    continue


                error_features = []                
                if feature.geometry().isMultipart() and check_multilines_per_linestring:
                    # Handle individual line_parts for a multilinestring
                    for line_part in feature.geometry().constParts():
                        if line_part.length() < minimum_length:
                            error_feature = cls.create_error_feature(QgisUtilities.linestring_to_geometry(line_part), feature['objectid'])
                            error_features.append(error_feature)
                else:
                    # Handle the feature as a whole
                    if feature.geometry().length() < minimum_length:
                        error_features.append(feature)

                for error_feature in error_features:
                    message = f"Feature with objectid '{error_feature['objectid']}' has a length of {round(error_feature.geometry().length(), 1)}m which is shorter than the minimum length of {minimum_length}m."
                    result = cls.create_result(
                        run_id, validation_code, severity, feature_class, error_feature, message,
                        cls.get_attribute(feature, 'country')
                    )
                    results.append(result)

        return results
