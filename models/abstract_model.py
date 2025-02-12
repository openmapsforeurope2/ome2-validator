from abc import ABC
from qgis.core import QgsGeometry

class AbstractModel(ABC):

    def as_param_dict(self, srid: int | None = None) -> dict:
        """Turns the model's attributes into a dict.
        
        PyDapper takes parameters from a dict to substitute placeholders in the query.
        This method creates mentioned dict.
        Some additional steps are done to enable to insertion of QgsGeometry into a PostGIS geometry column.
        QgsGeometry is converted to WKB, which can be understood by PostGIS.
        In addition an SRID may be passed, to enable explicitly setting the geometry SRID.

        Args:
            srid (int, optional): Optional EPSG code, which may be used by PostGIS for explicitly setting the geometry SRID. Defaults to None.

        Returns:
            dict: _description_
        """

        # Get properties as dict
        param_dict = vars(self)

        set_srid = False    
        # Prepare geometry for database insertion
        for key, value in param_dict.items():
            if type(value) in [QgsGeometry]: # More Qgs types could be allowed here (i.e. QgsPolygon) as long as they have the asWkb() method
                param_dict[key] = value.asWkb().data()
                set_srid = True
        
        # Add srid for geometry insert in PostGIS
        if set_srid and srid is not None:
            param_dict['srid'] = srid

        return param_dict
