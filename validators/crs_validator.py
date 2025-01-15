
from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar
from qgis.core import QgsVectorLayer, QgsCoordinateReferenceSystem, QgsGeometry
from models import ValidationResult
from . import FeatureValidator
import logging

import pydapper

class CrsValidator(FeatureValidator):
    logger = logging.getLogger(__name__)
    dsn: ClassVar[str | None] = None

    @classmethod
    def set_dsn(cls, dsn):
        """Sets the DSN

        Args:
            dsn (str): The Data Source Name
        """
        cls.dsn = dsn


    @dataclass
    class CrsQueryRecord:
        objectid: str
        srid: int
        geometry: QgsGeometry


        @classmethod
        def from_query_row(cls, objectid: str, srid: int, geometry: memoryview) -> CrsValidator.CrsQueryRecord:
            # Convert WKB geometry from PostGIS to QgsGeometry
            qgs_geometry = QgsGeometry()
            qgs_geometry.fromWkb(geometry.tobytes())     
            return cls(objectid, srid, qgs_geometry)


    @classmethod
    def validate(cls, run_id: int, validation_code: str, severity: str, feature_class: QgsVectorLayer, epsg_code: int, schema: str) -> list[ValidationResult]:
        results = []
        if cls.dsn is None:
            raise Exception('Data Source Name (dsn) has not been set')

        crs_string = f"EPSG:{epsg_code}"
        if not QgsCoordinateReferenceSystem(crs_string).isValid():
            log_message = f"Skipping {cls.__name__} on '{feature_class.name()}' since the expected CRS '{crs_string}' does not seem valid."
            cls.logger.warning(log_message)
            return results
        
        if not crs_string == feature_class.crs().authid():
            log_message = f"Featureclass '{feature_class.name()}' has CRS '{feature_class.crs().authid()}' but should have CRS '{crs_string}' according to the dataschema."
            cls.logger.warning(log_message)

        query_records = None
        commands = pydapper.connect(cls.dsn)
        try:
            with commands:
                query_records = commands.query(
                    f"SELECT objectid, \
                        ST_SRID(geom) as srid, \
                        ST_AsBinary(geom) as geometry \
                        FROM {schema}.{feature_class.name()} \
                        WHERE ST_SRID(geom) <> {epsg_code}",
                model = cls.CrsQueryRecord.from_query_row
                )

        finally:
            commands.connection.close() # type: ignore # close() *does exist* on connection object

        for record in query_records:
            error_feature = cls.create_error_feature(record.geometry, record.objectid)
            message = f"'{feature_class.name()}' object with objectid '{record.objectid}' has geometry in CRS 'EPSG:{record.srid}' while it was expected to be in CRS '{crs_string}'."
            result = cls.create_result(run_id, validation_code, severity, feature_class, error_feature, message)
            results.append(result)

        return results
