from models import ValidationResult
from validators import FeatureValidator
from qgis.core import QgsSpatialIndex, QgsVectorLayer
from utilities import QgisUtilities
import logging

class MustNotHaveDuplicatesValidator(FeatureValidator):
    logger = logging.getLogger(__name__)

    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer) -> list[ValidationResult]:
        """Runs the class MustNotHaveDuplicatesValidator.

        Topology validation for finding duplicates.
        Based on: https://github.com/qgis/QGIS/blob/master/src/plugins/topology/topolTest.cpp#L250

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class which should not have duplicate geometries.

        Returns:
            list[ValidationResult]: A list of results, containing the duplicate geometries.
        """
        results = []

        duplicate_ids = set()
    
        # Create index, store feature geometries so we can retrieve them later with index.geometry()
        index = QgsSpatialIndex(feature_class.getFeatures(), flags=QgsSpatialIndex.FlagStoreFeatureGeometries)

        # Loop over features
        for feature in feature_class.getFeatures():

            # Skip if already marked as duplicate
            if feature.id() in duplicate_ids:
                continue
            
            g1 = feature.geometry()
            # Check for valid geometry
            if QgisUtilities.is_empty_or_invalid_geometry(g1):
                log_message = cls.get_empty_or_invalid_geometry_message(feature_class, feature)
                cls.logger.warning(log_message)
                continue

            # Get all candidate features by intersecting against feature bounding box
            bb = g1.boundingBox()
            candidate_ids = index.intersects( bb )

            # Don't compare feature against its own geometry
            if (feature.id() in candidate_ids):
                candidate_ids.remove(feature.id())

            # Get all candidate features
            for candidate_id in candidate_ids:
                # Retrieve geometry via index
                g2 = index.geometry(candidate_id)

                # Check for valid geometry
                if QgisUtilities.is_empty_or_invalid_geometry(g2):
                    continue

                # Store feature id's of duplicates
                if ( g1.isGeosEqual( g2 ) ):
                    duplicate_ids.add(feature.id())
                    duplicate_ids.add(candidate_id)

        for duplicate_id in duplicate_ids:
            # Create feature of the duplicate geometry
            error_geom = index.geometry(duplicate_id)
            error_feature = cls.create_error_feature(error_geom, duplicate_id)
            message = f'{feature_class.name()} object with objectid {duplicate_id} is a duplicate geometry.'
            result = cls.create_result(run_id, validation_code, severity, feature_class, error_feature, message)
            results.append(result)

        return results
