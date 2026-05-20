from vrailang import *
from validation_specs.domains import *

begin_theme('BND', 'ib')

#region Featuretypes

class international_boundary_line(feature): 
   objectid: uuid[primary_key, notnull] 
   country: varchar[length(8)] 
   begin_lifespan_version: timestamp 
   end_lifespan_version: timestamp 
   w_national_identifier: varchar[length(255)] 
   xy_source: varchar[length(255)] 
   z_source: varchar[length(255)] 
   w_scale: varchar[length(80)] 
   w_release: int4 
   geom: LineString[srid(3035)] 
   boundary_type: varchar[length(255)] 
   legal_status: varchar[length(255)] 
   technical_status: varchar[length(255)] 
   boundary_source: varchar[length(255)] 

class international_boundary_node(feature): 
   objectid: uuid[primary_key, notnull] 
   country: varchar[length(8)] 
   begin_lifespan_version: timestamp 
   end_lifespan_version: timestamp 
   w_national_identifier: varchar[length(255)] 
   xy_source: varchar[length(255)] 
   z_source: varchar[length(255)] 
   w_scale: varchar[length(80)] 
   w_release: int4 
   geom: Point[srid(3035)] 
   legal_status: varchar[length(255)] 
   technical_status: varchar[length(255)] 

class landmask(feature): 
   objectid: uuid[primary_key, notnull] 
   country: varchar[length(8)] 
   begin_lifespan_version: timestamp 
   end_lifespan_version: timestamp 
   w_national_identifier: varchar[length(255)] 
   xy_source: varchar[length(255)] 
   z_source: varchar[length(255)] 
   w_scale: varchar[length(80)] 
   w_release: int4 
   geom: MultiPolygon[srid(3035)] 

#endregion


end_theme()
