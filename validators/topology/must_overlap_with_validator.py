from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsSpatialIndex, QgsVectorLayer
from utilities import QgisUtilities
import logging


class MustOverlapWithValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer,
                 feature_class_2: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the class MustOverlapWithValidator.

        Topology validation for finding overlaps with another layer
        Based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L846

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class which should have overlap with the other featureclass.
            feature_class_2 (QgsVectorLayer): The feature class which is used for comparison.

        Returns:
            list[ValidationResult]: A list of results, containing the geometry of areas that have no overlap with feature_class_2.
        """
        results = []

        skip_itself = feature_class == feature_class_2

        # Create index, store feature geometries so we can retrieve them later with index.geometry()
        index = QgsSpatialIndex(feature_class_2.getFeatures(), flags=QgsSpatialIndex.FlagStoreFeatureGeometries)

        # Loop over features
        for feature in feature_class.getFeatures():
            has_overlap = False
            g1 = feature.geometry()

            # Check for valid geometry
            if QgisUtilities.is_empty_or_invalid_geometry(g1):
                log_message = cls.get_empty_or_invalid_geometry_message(feature_class, feature)
                cls.logger.warning(log_message)
                continue

            # Get all candidate features by intersecting against feature bounding box
            bb = g1.boundingBox()
            candidate_ids = index.intersects(bb)
            for candidate_id in candidate_ids:
                # Don't compare feature against its own geometry, when invoked with the same layer
                if (skip_itself and feature.id() == candidate_id):
                    continue

                # Retrieve geometry via index
                g2 = index.geometry(candidate_id)

                # Check for valid geometry
                if QgisUtilities.is_empty_or_invalid_geometry(g2):
                    continue

                if g1.overlaps(g2):
                    has_overlap = True
                    break

            if not has_overlap:
                message = f'{feature_class.name()} object with objectid {feature.attribute("objectid")} has no overlap with object from {feature_class_2.name()}.'
                result = cls.create_result(run_id, validation_code, severity, feature_class, g1, message)
                results.append(result)

        return results
