from __future__ import annotations

from dataclasses import dataclass
from qgis.core import QgsGeometry, QgsVectorLayer, QgsCoordinateReferenceSystem, QgsFields, QgsField, QgsFeature
from qgis.PyQt.QtCore import QVariant
from . import ValidationResult
from collections import defaultdict

import logging


@dataclass
class GeometryResult(ValidationResult):
    """Dataclass for storing geometry results in the database.

        Most attributes are inherited of the abstract ValidationResult.
    
        Attributes:
        objectid (str): The id.
        geometry (QgsGeometry): The actual geometry. The QgsGeometry is converted to WKB by AbstractModel.as_param_dict() to allow for database insertion.
        geometry_type (str): The geometry type. This is handled by PostGIS on database insertion.
    """

    logger = logging.getLogger(__name__)

    objectid: str
    geometry: QgsGeometry
    geometry_type: str

    @classmethod
    def from_query_row(cls, result_id: int, run_id: int, validation_code: str, severity: str, feature_class: str, message: str, objectid: str, geometry: memoryview, geometry_type: str, country: str | None) -> GeometryResult:
        """Parses a geometry result record from the database into a GeometryResult object.

        Args:
            result_id (int): The result id.
            run_id (int): The run id.
            validation_code (str): The validation code.
            severity (str): The severity.
            feature_class (str): Name of the corresponding featureclass.
            message (str): The result message.
            objectid (str): Objectid of the corresponding source feature.
            geometry (memoryview): The actual geometry in WKB, which is about to be converted to a QgsGeometry.
            geometry_type (str): The geometry type as determined by PostGIS.
            country (str | None): The country.

        Returns:
            GeometryResult: the GeometryResult object
        """
        
        # Convert WKB geometry from PostGIS to QgsGeometry
        qgs_geometry = QgsGeometry()
        if geometry is not None:
            qgs_geometry.fromWkb(geometry.tobytes())       
        
        return cls(result_id, run_id, validation_code, severity, feature_class, message, country, objectid, qgs_geometry, geometry_type)
    

    def to_qgs_feature(self) -> QgsFeature:
        """Turns this geometry result into QgsFeature.

        Returns:
            QgsFeature: A feature representing a geometry result.
        """
        feature = QgsFeature()
        feature.setGeometry(self.geometry)
        fields = self.get_fields()
        feature.setFields(fields)
        attributes = self.get_attributes()
        feature.setAttributes(attributes)

        if len(fields) != len(attributes):
            self.logger.error("The number of fields and values for this features do not match.")
        return feature
    
    
    @classmethod
    def geometry_results_to_vector_layer_per_geom_type(cls, results: list[GeometryResult], name: str, epsg_code: str) -> list[QgsVectorLayer]:
        """Turns a list of GeometryResults into a list of VectorLayers.
         
        One VectorLayer is created per per geometry type since we can't combine multiple types in a single layer.

        Args:
            results (list[GeometryResult]): The geometry results.
            name (str): Base name of the vector layers to create. Gets the geometry type as postfix.
            epsg_code (str): The SRID of the geometry.

        Returns:
            list[QgsVectorLayer]: The created vector layers
        """
        layers = []

        # Group results by geometry type 
        results_per_geometry_type = defaultdict(list)
        for result in results:
            geom_type = result.geometry_type.replace("ST_","")
            results_per_geometry_type[geom_type].append(result)

        # Create a vectorlayer for each geometry type
        for geom_type, results in results_per_geometry_type.items():
            layer = GeometryResult.geometry_results_to_vector_layer(results, f"{name}_{geom_type}", geom_type, epsg_code)
            layers.append((geom_type, layer))

        return layers
    

    @classmethod
    def geometry_results_to_vector_layer(cls, geom_results: list[GeometryResult], name: str, geom_type: str, epsg_code: str) -> QgsVectorLayer:
        """Turns a list of GeometryResults into a VectorLayer.

        Note that all geometry results are expected to have the specified geometry type.

        Args:
            geom_results (list[GeometryResult]): he geometry results.
            name (str): Name of the vector layer to create.
            geom_type (str): The geometry type of the vector layer to create.
            epsg_code (str): The SRID of the geometry.

        Raises:
            ValueError: The given EPSG code should be known to QGIS.
            ValueError: The given geometry type should be supported.

        Returns:
            QgsVectorLayer: The created vector layer
        """
        crs = QgsCoordinateReferenceSystem(epsg_code)
        if not crs.isValid():
            raise ValueError(f"EPSG code {epsg_code} is not supported.")

        allowed_geometry_types = ["Point", "LineString", "Polygon", "MultiPoint", "MultiLineString", "MultiPolygon"]
        if geom_type not in allowed_geometry_types:
            raise ValueError(f"Geometry type {geom_type} is not supported.")
        

        layer = QgsVectorLayer(geom_type, name, "memory")
        layer.setCrs(crs, True)
        data_provider = layer.dataProvider()
        fields = cls.get_fields()
        data_provider.addAttributes(fields)
        layer.updateFields()        

        features = [geom_result.to_qgs_feature() for geom_result in geom_results]
        data_provider.addFeatures(features)
        if (data_provider.hasErrors()):
            cls.logger.error(f"Something went wrong while turning geometry results into vector layer {layer.name()}. {data_provider.errors()}")

        return layer
    
    @classmethod
    def get_fields(cls) -> QgsFields:
        """Returns a QgsFields object which describe a GeometryResult.

        Note that these fields should match the amount and order of the get_attributes() method.

        Returns:
            QgsFields: the fields.
        """
        new_fields = QgsFields()
        new_fields.append(QgsField("result_id", QVariant.Int))
        new_fields.append(QgsField("run_id", QVariant.Int))
        new_fields.append(QgsField("validation_code", QVariant.String))
        new_fields.append(QgsField("severity", QVariant.String))
        new_fields.append(QgsField("feature_class", QVariant.String))
        new_fields.append(QgsField("message", QVariant.String))
        new_fields.append(QgsField("objectid", QVariant.String))
        new_fields.append(QgsField("geometry_type", QVariant.String))
        new_fields.append(QgsField("country", QVariant.String))
        return new_fields
    
    
    def get_attributes(self) -> list[object]:
        """Returns a list of values of a GeometryResult.

        Note that these values should match the amount and order of the get_fields() method.

        Returns:
            list[object]: the values.
        """
        return [
            self.result_id,
            self.run_id,
            self.validation_code,
            self.severity,
            self.feature_class,
            self.message,
            self.objectid,
            self.geometry_type,
            self.country
            ]
