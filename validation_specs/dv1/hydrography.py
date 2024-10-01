from vrailang import *

begin_theme('HYDRO', 'hy')

#region Featuretypes

#region Hydrographic network

class watercourse_link(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: LineStringZ[srid(3035)]
    level: varchar[length(255)]
    persistence: varchar[length(255)]
    tidal: varchar[length(255)]
    flow_direction: varchar[length(255)]
    stream_order: varchar[length(255)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    origin: varchar[length(255)]
    fictitious: varchar[length(255)]
    tent_network: varchar[length(255)]
    cemt_class: varchar[length(255)]
    navigable: varchar[length(255)]
    width_lower_range: int4
    width_upper_range: int4


class watercourse(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiLineStringZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class hydro_node(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    hydro_node_category: varchar[length(255)]


#endregion

#region Other hydrographic features 

class dam_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class dam_line(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: LineStringZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class dam_point(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class falls_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]


class falls_line(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: LineStringZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]


class falls_point(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]


class lock_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class lock_line(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: LineStringZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class lock_point(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class watercourse_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    persistence: varchar[length(255)]
    tidal: varchar[length(255)]
    origin: varchar[length(255)]


class standing_water(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    persistence: varchar[length(255)]
    tidal: varchar[length(255)]
    origin: varchar[length(255)]


class shoreline(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: LineStringZ[srid(3035)]
    water_level: varchar[length(255)]
    origin: varchar[length(255)]


class shore(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    composition: varchar[length(255)]


class drainage_basin(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: LineStringZ[srid(3035)]
    hydro_identifier: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    basin_order: varchar[length(255)]


class glacier_snowfield(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    ice_area_type: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class shoreline_construction_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    shoreline_construction_type: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class shoreline_construction_line(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: LineStringZ[srid(3035)]
    shoreline_construction_type: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]


class wetland(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    local_name: varchar[length(255)]
    tidal: varchar[length(255)]

#endregion

#endregion


end_theme()
