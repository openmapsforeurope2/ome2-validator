from abc import ABC, abstractmethod
from typing import ClassVar
from models import ValidationCheckStatus, ValidationResult
from storage import ValidationCheckStatusRepository
from qgis.core import QgsGeometry, QgsFeature, QgsFields, QgsField, QgsVectorLayer, QgsWkbTypes
from qgis.PyQt.QtCore import QVariant
import datetime
import logging
import traceback

from storage.result_repository_protocol import ResultRepositoryProtocol

class AbstractValidator(ABC):
    result_repository: ClassVar[type[ResultRepositoryProtocol]]
    logger = logging.getLogger(__name__)

    @classmethod
    def run(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, *args, **kwargs):
        """A wrapper method to start the validation of a validator.

        This method ensures that:
          1. a ValidationCheckStatus is created before the actual validation logic is started.
          2. the validation logic is started by calling the validate() function.
          3. in case of success, the validation results are stored in the corresponding repository (being either the GeometryResultRepository or GenericResultRepository, depending on the Validator type).
          4. the ValidationCheckStatus is updated, both in case of success or failure.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
        """

        # Typed nulls for satisfying the typechecker
        GENERATE_DATE: datetime.date = None  # type: ignore

        check_status = ValidationCheckStatus(validation_code, run_id, 
                                             GENERATE_DATE, GENERATE_DATE, GENERATE_DATE, 
                                             None, -1)
        exception = False
        validation_results: list[ValidationResult] = []
        try:
            cls.logger.info(f'Start running the {cls.__name__} for {validation_code}')
            ValidationCheckStatusRepository.add(check_status)
            validation_results = cls.validate( run_id, validation_code, severity, feature_class, *args, **kwargs)
        except Exception:
            exception = True
            cls.logger.error(f'An exception occured while running the {cls.__name__} for {validation_code}:')
            for line in traceback.format_exc(limit=8).splitlines():
                cls.logger.error(line)
            check_status.success = False
            ValidationCheckStatusRepository.update_on_end(check_status)
        finally:
            if not exception:
                cls.logger.info(f'Finished running the {cls.__name__} for {validation_code}')
                check_status.success = True
                check_status.number_of_results = len(validation_results)
                cls.logger.info(f'Number of results for {validation_code}: {check_status.number_of_results}')

                try:
                    cls.result_repository.add_list(validation_results)
                except Exception:
                    cls.logger.error(f'An exception occured while storing validation results of the {cls.__name__} for {validation_code}:')
                    for line in traceback.format_exc(limit=8).splitlines():
                        cls.logger.error(line)

                ValidationCheckStatusRepository.update_on_end(check_status)


    @classmethod
    @abstractmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, *args, **kwargs) -> list[ValidationResult]:
        """Abstract method for the actual validation logic.

        Args:
            run_id (int): The id of the current run.
            validation_code (str): The validation code to use.
            severity (str): The severity to use (WARNING / ERROR / STATISTIC).
            feature_class (QgsVectorLayer): The feature class to check.
        Returns:
            list[ValidationResult]: A list of results
        """        
        pass


    @classmethod
    def create_error_feature(cls, geometry: QgsGeometry, objectid: str = '00000000-0000-0000-0000-000000000000') -> QgsFeature:
        """Creates an error feature 

        In certain validators the validation result does not contain an actual feature, but a newly constructed geometry.
        This method is used to turn this geometry into a QgsFeature which can then be used to create a GeometryResult.
        In some cases (i.e. MustNothaveGapsValidator) the result does not correspond to a single source object, in which case a default UUID placeholder is used as objectid.

        Args:
            geometry (QgsGeometry): The geometry
            objectid (str, optional): The objectid of this error feature. Defaults to '00000000-0000-0000-0000-000000000000'.

        Returns:
            QgsFeature: A QgsFeature with geometry and an objectid, which can be used to create a GeometryResult.
        """
        error_feature = QgsFeature()
        new_fields = QgsFields()
        new_fields.append(QgsField("objectid", QVariant.String))
        error_feature.setFields(new_fields)
        error_feature.setAttribute(0, objectid)
        error_feature.setGeometry(geometry)
        return error_feature
    

    @classmethod
    def get_invalid_geometry_type_message(cls, feature_class: QgsVectorLayer, valid_geometry_types: list[QgsWkbTypes.GeometryType]) -> str:
        """Creates a message when validation on a featureclass is skipped because of an unexpected geometry type.

        Args:
            feature_class (QgsVectorLayer): The featureclass with the unexpected geometry type.
            valid_geometry_types (list[QgsWkbTypes.GeometryType]): The expected geometry types.

        Returns:
            str: A message describing the unexpected geometry type of the featureclass.
        """        
        valid_types_string = ' or '.join([QgsWkbTypes.geometryDisplayString(type) for type in valid_geometry_types])
        return f"Skipping {cls.__name__} on '{feature_class.name()}' since the geometry type is not {valid_types_string} but {QgsWkbTypes.geometryDisplayString(feature_class.geometryType())}."

    
    @classmethod
    def get_empty_or_invalid_geometry_message(cls, feature_class: QgsVectorLayer, feature: QgsFeature) -> str:
        """Creates a message when validation on a feature is skipped because of empty or invalid geometry.

        Args:
            feature_class (QgsVectorLayer): The featureclass which contains a feature with empty of invalid geometry.
            feature (QgsFeature): A feature with empty or invalid geometry.

        Returns:
            str: A message describing the empty of invalid geometry of the feature.
        """        
        return f"Skipping {cls.__name__} on '{feature_class.name()}' feature with objectid '{feature['objectid']}' since the geometry is empty or invalid." 
