from vrailang import *
from validation_specs.domains import *
begin_theme('TRANS', 'tn')


#region Featuretypes

#region Road network

class road_link(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: LineStringZ[srid(3035)]
    form_of_way: varchar[length(255)]
    functional_road_class: varchar[length(255)]
    number_of_lanes: varchar[length(255)]
    vertical_position: varchar[length(255)]
    vertical_level: varchar[length(255)]
    tent_network: varchar[length(255)]
    street_name: jsonb
    street_label: varchar[length(255)]
    road_surface_category: varchar[length(255)]
    traffic_flow_direction: varchar[length(255)]
    access_restriction: varchar[length(255)]
    restriction_for_vehicles: jsonb
    speed_limit: int4
    condition_of_facility: varchar[length(255)]
    link_to_road: varchar[length(255)]
    road_national_road_code: varchar[length(255)]
    road_european_route_number: varchar[length(255)]
    road_name: jsonb
    road_label: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4


class road(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiLineStringZ[srid(3035)]
    national_road_code: varchar[length(255)]
    european_route_number: varchar[length(255)]
    road_name: jsonb
    road_label: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4


class road_node(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    name: jsonb
    form_of_road_node: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class road_service_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    type: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class road_service_point(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    type: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class marker_post(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    link_to_road: varchar[length(255)]
    code: varchar[length(255)]
    distance: real
    w_link_to_national_road: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4


#endregion


#region Railway network

class railway_link(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: LineStringZ[srid(3035)]
    type: varchar[length(255)]
    number_of_tracks: varchar[length(255)]
    vertical_position: varchar[length(255)]
    vertical_level: varchar[length(255)]
    tent_network: varchar[length(255)]
    electrified: varchar[length(255)]
    condition_of_facility: varchar[length(255)]
    railway_line_code: varchar[length(255)]
    railway_line_name: jsonb
    railway_line_label: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class railway_line(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiLineStringZ[srid(3035)]
    railway_line_code: varchar[length(255)]
    raliway_line_name: jsonb
    raliway_line_label: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4


class railway_station_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    station_code: varchar[length(255)]
    railway_use: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4


class railway_station_point(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    station_code: varchar[length(255)]
    railway_use: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

#endregion





#region Air transport

class aerodrome_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    designator_iata: varchar[length(255)]
    location_indicator_icao: varchar[length(255)]
    un_locode: varchar[length(255)]
    name: jsonb
    aerodrome_category: varchar[length(255)]
    aerodrome_type: varchar[length(255)]
    use_restriction: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class aerodrome_point(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    designator_iata: varchar[length(255)]
    location_indicator_icao: varchar[length(255)]
    un_locode: varchar[length(255)]
    name: jsonb
    aerodrome_category: varchar[length(255)]
    aerodrome_type: varchar[length(255)]
    use_restriction: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4


class runway_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygonZ[srid(3035)]
    surface_composition: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4


class runway_line(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiLineStringZ[srid(3035)]
    surface_composition: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

#endregion



#region Water transport


class ferry_crossing(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiLineStringZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    ferry_use: varchar[length(255)]
    tent_network: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4


class port_area(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygon[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    un_locode: varchar[length(255)]
    tent_network: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class port_point(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    un_locode: varchar[length(255)]
    tent_network: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4


#endregion


#endregion


# General content
#T001 = runway_line.MustComplyWithDataschema()

T001 = road_link.MustComplyWithDataschema()
T002 = road.MustComplyWithDataschema()
T003 = road_node.MustComplyWithDataschema()
T004 = road_service_area.MustComplyWithDataschema()
T005 = road_service_point.MustComplyWithDataschema()
T006 = marker_post.MustComplyWithDataschema()
T007 = railway_link.MustComplyWithDataschema()
T008 = railway_line.MustComplyWithDataschema()
T009 = railway_station_area.MustComplyWithDataschema()
T010 = railway_station_point.MustComplyWithDataschema()
T011 = aerodrome_area.MustComplyWithDataschema()
T012 = aerodrome_point.MustComplyWithDataschema()
T013 = runway_area.MustComplyWithDataschema()
T014 = runway_line.MustComplyWithDataschema()
T015 = ferry_crossing.MustComplyWithDataschema()
T016 = port_area.MustComplyWithDataschema()
T017 = port_point.MustComplyWithDataschema()

# # Geometric resolution
# T002 = runway_line.geom.MustHaveCorrectCRS()
# T003 = runway_line.MustHaveValidGeometry()
# T004 = runway_line.geom.MustHaveCorrectGeometryType()
# T005 = runway_line.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()

# Data model and attribute resolution
# T010 = runway_line.objectid.MustNotBeNull()

# TODO checks on road_link are very slow
# T020 = road_link.form_of_way.MustBeOfValues(FormOfWayValue.to_list())
# T021 = road_link.functional_road_class.MustBeOfValues(FunctionalRoadClass.to_list())
# T022 = road_link.vertical_position.MustBeOfValues(VerticalPositionValue.to_list())
# T023 = road_link.road_surface_category.MustBeOfValues(RoadSurfaceCategoryValue.to_list())
# T024 = road_link.tent_network.MustBeOfValues(TENTNetworkValue.to_list())
# T025 = road_link.traffic_flow_direction.MustBeOfValues(TrafficFlowDirectionValue.to_list())
# T026 = road_link.access_restriction.MustBeOfValues(AccessRestrictionValue.to_list())
# T027 = road_node.form_of_road_node.MustBeOfValues(FormOfRoadNodeValue.to_list())
# T028 = road_service_point.type.MustBeOfValues(RoadServiceTypeValue.to_list())
# T029 = road_service_area.type.MustBeOfValues(RoadServiceTypeValue.to_list())
# T030 = railway_link.type.MustBeOfValues(RailwayTypeValue.to_list())
# T031 = railway_link.electrified.MustBeOfValues(ElectrifiedValue.to_list())
# T032 = railway_station_point.railway_use.MustBeOfValues(RailwayStationUseValue.to_list())
# T033 = railway_station_area.railway_use.MustBeOfValues(RailwayStationUseValue.to_list())
# T034 = aerodrome_point.aerodrome_category.MustBeOfValues(AerodromeCategoryValue.to_list())
# T035 = aerodrome_area.aerodrome_category.MustBeOfValues(AerodromeCategoryValue.to_list())
# T036 = aerodrome_point.aerodrome_type.MustBeOfValues(AerodromeTypeValue.to_list())
# T037 = aerodrome_area.aerodrome_type.MustBeOfValues(AerodromeTypeValue.to_list())
# T038 = aerodrome_point.use_restriction.MustBeOfValues(UseRestrictionValue.to_list())
# T039 = aerodrome_area.use_restriction.MustBeOfValues(UseRestrictionValue.to_list())
# T040 = runway_line.surface_composition.MustBeOfValues(SurfaceCategoryValue.to_list())
# T041 = runway_area.surface_composition.MustBeOfValues(SurfaceCategoryValue.to_list())
# T042 = ferry_crossing.ferry_use.MustBeOfValues(FerryUseValue.to_list())
# T043 = ferry_crossing.tent_network.MustBeOfValues(TENTNetworkValue.to_list())
# T044 = port_point.tent_network.MustBeOfValues(TENTNetworkValue.to_list())
# T045 = port_area.tent_network.MustBeOfValues(TENTNetworkValue.to_list())

end_theme()

