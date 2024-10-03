import os
import sys

if os.name == 'nt':
    # Set paths based on location of Python executable:
    apps_py_dir = os.path.dirname(sys.executable)
    pyqgis_path = os.path.abspath(os.path.join(apps_py_dir, '../qgis/python'))
    pyqgis_plugins_path = os.path.join(pyqgis_path, 'plugins')
    qgis_dir = os.path.abspath(os.path.join(apps_py_dir, '../..'))
    qgis_bin_dir = os.path.join(qgis_dir, 'bin')

    sys.path.append(pyqgis_path)
    sys.path.append(pyqgis_plugins_path)
    os.add_dll_directory(qgis_bin_dir)


from qgis.core import *
from qgis import processing
from qgis.PyQt.QtCore import QMetaType

import logging

class QgisUtilities:
    logger = logging.getLogger(__name__)

    qgs = QgsApplication([], GUIenabled=False)
    uri = QgsDataSourceUri()
    
    @classmethod
    def initialize_qgis(cls):
        """Initialize QGIS to load the QGIS data providers and layer registry.
        """        
        cls.qgs.initQgis()
        from processing.core.Processing import Processing
        Processing.initialize()

    @classmethod
    def exit_qgis(cls):
        """Exit QGIS to remove the data providers and layer registry from memory.
        """        
        cls.qgs.exitQgis()

    @classmethod
    def get_version(cls) -> str:
        """Gets the QGIS version.

        Returns:
            str: The QGIS version.
        """        
        return Qgis.QGIS_VERSION

    @classmethod
    def get_release_name(cls) -> str:
        """Gets the QGIS release name.

        Returns:
            str: The QGIS release name.
        """        
        return Qgis.QGIS_RELEASE_NAME


    @classmethod
    def setup_postgis_connection(cls, host: str, port: int, database: str, username: str, password: str):
        """Sets up the connection to the PostGIS database containing the input data.

        Args:
            host (str): The host.
            port (int): The port.
            database (str): The database name.
            username (str): The username.
            password (str): The password.
        """        
        cls.uri.setConnection(host, str(port), database, username, password, QgsDataSourceUri.SslPrefer)


    @classmethod
    def create_postgres_vector_layer(cls, schema: str, table_name: str, geometry_column: str, sql: str = '', key_column: str = '', layer_name: str = None) -> QgsVectorLayer:
        """Creates a vectorlayer based on a PostGIS table.

        TODO Test using 'objectid' as key_column for OME2 data. This may enable using feature.id() in stead of feature['objectid']?

        Args:
            schema (str): The schema.
            table_name (str): The table.
            geometry_column (str): The column containing the geometry.
            sql (str, optional): Optional where-clause to limit the selection of objects. Defaults to ''.
            key_column (str, optional): The primary key column. Defaults to ''.
            layer_name (str, optional): The name of the output vectorlayer. Defaults to None, in which case the table name is used.

        Returns:
            QgsVectorLayer: The created vector layer.
        """        
        layer_name =  table_name if layer_name is None else layer_name
        cls.uri.setDataSource(schema, table_name, geometry_column, sql, key_column)
        
        vector_layer = QgsVectorLayer(cls.uri.uri(False), layer_name, "postgres")
        if not vector_layer.isValid():
            cls.logger.warning(f"Could not create PostGreSQL layer based on table: {table_name}.")

        return vector_layer


    @classmethod
    def get_layer_fields(cls, layer: QgsVectorLayer) -> list[tuple[str, str]]:
        """Gets the name and type of a layer's fields.

        Args:
            layer (QgsVectorLayer): The layer of which we want to get the fields.

        Returns:
            list[tuple[str, str]]: A list of tuples, containing field name and type.
        """      
        layer_fields = []
        for field in layer.fields():
            layer_fields.append((field.name(),field.typeName()))
        return layer_fields
    

    @classmethod
    def polygon_to_geometry(cls, polygon: QgsPolygon) -> QgsGeometry:
        """Converts a QgsPolygon to a QgsGeometry

        Args:
            polygon (QgsPolygon):the input polygon.

        Returns:
            QgsGeometry: the output geometry.
        """        
        return QgsGeometry.fromWkt(polygon.asWkt())
    
    
    @classmethod
    def linestring_to_geometry(cls, linestring: QgsLineString) -> QgsGeometry:
        """Converts a QgsLineString to a QgsGeometry

        Args:
            linestring (QgsLineString): the input linestring.

        Returns:
            QgsGeometry: the output geometry.
        """        
        return QgsGeometry.fromWkt(linestring.asWkt())
    

    @classmethod
    def pointxy_to_geometry(cls, point_xy: QgsPointXY) -> QgsGeometry:
        """Converts a QgsPointXY to a QgsGeometry

        Args:
            point_xy (QgsPointXY): the input point.

        Returns:
            QgsGeometry: the output geometry.
        """        
        return QgsGeometry.fromPointXY(point_xy)


    @classmethod
    def geometry_to_polyline_list(cls, geometry: QgsGeometry) -> list[list[QgsPoint]]:
        """Converts a QgsGeometry of type Line to a list of polylines (being list[QgsPoints]).

        Args:
            geometry (QgsGeometry): The input geometry.

        Raises:
            TypeError: Thrown if the input is not a QgsGeometry of type Line.

        Returns:
            list[list[QgsPoint]]: a list of polylines (list[QgsPoints]).
        """        
        if not type(geometry) == QgsGeometry or not geometry.type() == QgsWkbTypes.GeometryType.LineGeometry:
            raise TypeError("geometry must be a QgsGeometry of type Line")
        
        polylines = []
        if geometry.isMultipart():
            polylines.extend(geometry.asMultiPolyline())
        else:
            polylines.append(geometry.asPolyline())
        return polylines

        
    @classmethod
    def geometry_to_point_list(cls, geometry: QgsGeometry) -> list[QgsPoint]:
        """Converts a QgsGeometry of type Point to a flat list of QgsPoints.

        Used to handle mutlipoint geometry.

        Args:
            geometry (QgsGeometry): The input geometry.

        Raises:
            TypeError: Thrown if the input is not a QgsGeometry of type Point.

        Returns:
            list[QgsPoint]: a list of QgsPoints.
        """        
        if not type(geometry) == QgsGeometry or not geometry.type() == QgsWkbTypes.GeometryType.PointGeometry:
            raise TypeError("geometry must be a QgsGeometry of type Point")
        
        points = []
        if geometry.isMultipart():
            points.extend(geometry.asMultiPoint())
        else:
            points.append(geometry.asPoint())    
        return points
    

    @classmethod
    def is_empty_or_invalid_geometry(cls, geometry: QgsGeometry) -> bool:
        """Checks if the geometry if empty or invalid.

        Args:
            geometry (QgsGeometry): the geometry to check.

        Raises:
            TypeError: Thrown if the input value is not a QgsGeometry.

        Returns:
            bool: True if the geometry is empty or invalid.
        """        
        if not type(geometry) == QgsGeometry:
            raise TypeError("geometry must be a QgsGeometry")
        return geometry.isNull() or geometry.isEmpty() or not geometry.isGeosValid()


    @classmethod
    def export_vector_layer(cls, layer: QgsVectorLayer, ogr_driver: str) -> bool:
        """Exports the layer using the specified driver.

        Note that the name property of the vectorlayer is also used as the file name for the export.

        Args:
            layer (QgsVectorLayer): The layer to be exported.
            ogr_driver (str): The driver that's reponsible for this export, i.e.: 'GeoPackage', 'ESRI Shapefile', 'GeoJSON' or 'Geography Markup Language [GML]'.

        Raises:
            TypeError: Thrown if an unknown driver is specified.

        Returns:
            bool: True if the export was successful.
        """        
        # Look for a matching OGR driver
        matching_drivers = list(filter(lambda d: d.longName.lower() == ogr_driver.lower(), QgsVectorFileWriter.ogrDriverList()))
        if len(matching_drivers) == 0:
            raise TypeError(f"OGR driver '{ogr_driver}' is not supported.")
        matching_driver = matching_drivers[0]
        
        export_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exports')
        file_name = f"{export_dir}\\{layer.name()}"

        save_options = QgsVectorFileWriter.SaveVectorOptions()
        save_options.driverName = matching_driver.driverName

        transform_context = QgsProject.instance().transformContext()
        cls.logger.info(f"Creating export of layer {layer.name()} using driver {matching_driver.longName}...")
        error = QgsVectorFileWriter.writeAsVectorFormatV3(layer,
                                                   file_name,
                                                   transform_context,
                                                   save_options)
        
        success = error[0] == QgsVectorFileWriter.NoError
        if success:
            cls.logger.info(f"Export created at {error[2]} ")
        else:
            cls.logger.error(f"Export failed: {error[0]}")
        
        return success
    

    @classmethod
    def merge_vector_layers(cls, layers: list[QgsVectorLayer], merge_layer_name: str = "") -> QgsVectorLayer:
        """Merges several vectorlayers into a single vectorlayer.

        Args:
            layers (list[QgsVectorLayer]): The vectorlayers to be merged. These must have the same geometry type.
            merge_layer_name (str, optional): The name of the merged layer. Defaults to "", in which case a concatenation of the input layer names will be used.

        Raises:
            TypeError: Thrown if the input layers do not have the same geometry type.

        Returns:
            QgsVectorLayer: The merged vectorlayer.
        """

        # QGIS can only merge layers of the same geometry type
        geometry_types = set([layer.geometryType() for layer in layers])
        if len(geometry_types) > 1:
            raise TypeError("Cannot merge layers with different geometry types.")
        
        # QGIS cannot merge layers with PostgreSQL datatype jsonb, such as 'name'
        # Therefore we prepare layers by skipping certain fields
        prepared_layers = []
        for layer in layers:
            prepared_layer = QgisUtilities.create_memory_layer(layer, skip_field_types = [QMetaType.QVariantMap])
            prepared_layers.append(prepared_layer)

        # Run the merge algorithm
        cls.logger.info(f"Start merging layers {', '.join([layer.name() for layer in layers])} ...")
        parameters = {
            'LAYERS':prepared_layers,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        merge = processing.run("native:mergevectorlayers", parameters) # Run processing.algorithmHelp("native:mergevectorlayers") for documentation
        merge_layer = merge['OUTPUT']
        cls.logger.info(f"Finished merging layers.")

        # Set the layername
        if merge_layer_name == "":
            merge_layer_name = f"{'_'.join([layer.name() for layer in layers])}_merged"
        merge_layer.setName(merge_layer_name)
        
        return merge_layer
    
    
    @classmethod
    def create_memory_layer(cls, layer: QgsVectorLayer, skip_field_types: list[QMetaType.Type] = [], skip_field_names: list[str] = []):
        """Creates a memory layer based of an existing vectorlayer, with the possibility of skipping certain fields by type or name.

        This is mainly used to copy a vectorlayer while skipping certain fields, since they may prevent QGIS from using algorithms on the layer.
        For example, many layers in the OME2 data contain a field 'name' of datatype jsonb.
        This causes issues when running the 'native:buffer' or 'native:mergevectorlayers' algorithms.

        Args:
            layer (QgsVectorLayer): The input vector layer.
            skip_field_types (list[QMetaType.Type], optional): Field types which we do not want in the output memory layer. Defaults to [].
            skip_field_names (list[str], optional): Field names which we do not want in the output memory layer. Defaults to [].

        Returns:
            _type_: The output vectorlayer in memory.
        """        
        # Determine geometry type, crs and new layer name
        geom_type_string = QgsWkbTypes.displayString(layer.wkbType())
        crs_auth_id = layer.sourceCrs().authid()
        layer_name = f"{layer.name()}_memory"

        # Duplicate the input layer as a memory layer
        new_layer = QgsVectorLayer(f"{geom_type_string}?crs={crs_auth_id}", layer_name, "memory")
        data_provider = new_layer.dataProvider()

        # Filter fields based on skipped data types and field names
        filtered_fields = [field for field in layer.dataProvider().fields().toList()
                           if field.type() not in skip_field_types
                           and field.name() not in skip_field_names]
        data_provider.addAttributes(filtered_fields)
        new_layer.updateFields()
        
        all_features = [feature for feature in layer.getFeatures()] 
        # Remove the skipped fields on each feature
        for feature in all_features:
            all_fields = feature.fields()
            all_attrs = feature.attributes()
            new_fields = QgsFields()
            new_attrs = []
            
            for i in range(0, len(all_fields)-1):
                curr_field = all_fields[i]
                curr_attr = all_attrs[i]

                if curr_field.name() in [field.name() for field in filtered_fields] :
                    # Fill new fields and values
                    new_fields.append(curr_field)
                    new_attrs.append(curr_attr)

            # Set new fields and values on the feature
            feature.setFields(new_fields)
            feature.setAttributes(new_attrs)

        data_provider.addFeatures(all_features)
        if (data_provider.hasErrors()):
            cls.logger.error(f"Something went wrong while creating a memory layer for {layer.name()}. {data_provider.errors()}")

        return new_layer


    @classmethod
    def layer_has_field(cls, layer: QgsVectorLayer, field_name: str):
        """ Checks if a given field name exists on the given layer.

        Args:
            layer (QgsVectorLayer): The vector layer to check.
            attribute (str): The field name.

        Returns:
            bool: True if the field exists on this layer.
        """
        return layer.fields().indexFromName(field_name) > -1
