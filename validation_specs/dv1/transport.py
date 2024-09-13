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

#region Validation checks

#region General content

T001a = road_link.MustComplyWithDataschema()
T001b = road.MustComplyWithDataschema()
T001c = road_node.MustComplyWithDataschema()
T001d = road_service_area.MustComplyWithDataschema()
T001e = road_service_point.MustComplyWithDataschema()
T001f = marker_post.MustComplyWithDataschema()
T001g = railway_link.MustComplyWithDataschema()
T001h = railway_line.MustComplyWithDataschema()
T001i = railway_station_area.MustComplyWithDataschema()
T001j = railway_station_point.MustComplyWithDataschema()
T001k = aerodrome_area.MustComplyWithDataschema()
T001l = aerodrome_point.MustComplyWithDataschema()
T001m = runway_area.MustComplyWithDataschema()
T001n = runway_line.MustComplyWithDataschema()
T001o = ferry_crossing.MustComplyWithDataschema()
T001p = port_area.MustComplyWithDataschema()
T001q = port_point.MustComplyWithDataschema()

#endregion

# region Geometric resolution
T002a = road_link.geom.MustHaveCorrectCRS()
T002b = road.geom.MustHaveCorrectCRS()
T002c = road_node.geom.MustHaveCorrectCRS()
T002d = road_service_area.geom.MustHaveCorrectCRS()
T002e = road_service_point.geom.MustHaveCorrectCRS()
T002f = marker_post.geom.MustHaveCorrectCRS()
T002g = railway_link.geom.MustHaveCorrectCRS()
T002h = railway_line.geom.MustHaveCorrectCRS()
T002i = railway_station_area.geom.MustHaveCorrectCRS()
T002j = railway_station_point.geom.MustHaveCorrectCRS()
T002k = aerodrome_area.geom.MustHaveCorrectCRS()
T002l = aerodrome_point.geom.MustHaveCorrectCRS()
T002m = runway_area.geom.MustHaveCorrectCRS()
T002n = runway_line.geom.MustHaveCorrectCRS()
T002o = ferry_crossing.geom.MustHaveCorrectCRS()
T002p = port_area.geom.MustHaveCorrectCRS()
T002q = port_point.geom.MustHaveCorrectCRS()


T003a = road_link.geom.MustHaveCorrectGeometryType()
T003b = road.geom.MustHaveCorrectGeometryType()
T003c = road_node.geom.MustHaveCorrectGeometryType()
T003d = road_service_area.geom.MustHaveCorrectGeometryType()
T003e = road_service_point.geom.MustHaveCorrectGeometryType()
T003f = marker_post.geom.MustHaveCorrectGeometryType()
T003g = railway_link.geom.MustHaveCorrectGeometryType()
T003h = railway_line.geom.MustHaveCorrectGeometryType()
T003i = railway_station_area.geom.MustHaveCorrectGeometryType()
T003j = railway_station_point.geom.MustHaveCorrectGeometryType()
T003k = aerodrome_area.geom.MustHaveCorrectGeometryType()
T003l = aerodrome_point.geom.MustHaveCorrectGeometryType()
T003m = runway_area.geom.MustHaveCorrectGeometryType()
T003n = runway_line.geom.MustHaveCorrectGeometryType()
T003o = ferry_crossing.geom.MustHaveCorrectGeometryType()
T003p = port_area.geom.MustHaveCorrectGeometryType()
T003q = port_point.geom.MustHaveCorrectGeometryType()

T004a = road_link.MustHaveValidGeometry()
T004b = road.MustHaveValidGeometry()
T004c = road_node.MustHaveValidGeometry()
T004d = road_service_area.MustHaveValidGeometry()
T004e = road_service_point.MustHaveValidGeometry()
T004f = marker_post.MustHaveValidGeometry()
T004g = railway_link.MustHaveValidGeometry()
T004h = railway_line.MustHaveValidGeometry()
T004i = railway_station_area.MustHaveValidGeometry()
T004j = railway_station_point.MustHaveValidGeometry()
T004k = aerodrome_area.MustHaveValidGeometry()
T004l = aerodrome_point.MustHaveValidGeometry()
T004m = runway_area.MustHaveValidGeometry()
T004n = runway_line.MustHaveValidGeometry()
T004o = ferry_crossing.MustHaveValidGeometry()
T004p = port_area.MustHaveValidGeometry()
T004q = port_point.MustHaveValidGeometry()


T006n = runway_line.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()

#endregion

#region Data model and attribute resolution
T011a = road_link.objectid.MustNotBeNull()
T011b = road.objectid.MustNotBeNull()
T011c = road_node.objectid.MustNotBeNull()
T011d = road_service_area.objectid.MustNotBeNull()
T011e = road_service_point.objectid.MustNotBeNull()
T011f = marker_post.objectid.MustNotBeNull()
T011g = railway_link.objectid.MustNotBeNull()
T011h = railway_line.objectid.MustNotBeNull()
T011i = railway_station_area.objectid.MustNotBeNull()
T011j = railway_station_point.objectid.MustNotBeNull()
T011k = aerodrome_area.objectid.MustNotBeNull()
T011l = aerodrome_point.objectid.MustNotBeNull()
T011m = runway_area.objectid.MustNotBeNull()
T011n = runway_line.objectid.MustNotBeNull()
T011o = ferry_crossing.objectid.MustNotBeNull()
T011p = port_area.objectid.MustNotBeNull()
T011q = port_point.objectid.MustNotBeNull()

# TODO checks on road_link are very slow
T014a = road_link.form_of_way.MustBeOfValues(FormOfWayValue.to_list())
T014b = road_link.functional_road_class.MustBeOfValues(FunctionalRoadClass.to_list())
T014c = road_link.vertical_position.MustBeOfValues(VerticalPositionValue.to_list())
T014d = road_link.road_surface_category.MustBeOfValues(RoadSurfaceCategoryValue.to_list())
T014e = road_link.tent_network.MustBeOfValues(TENTNetworkValue.to_list())
T014f = road_link.traffic_flow_direction.MustBeOfValues(TrafficFlowDirectionValue.to_list())
T014g = road_link.access_restriction.MustBeOfValues(AccessRestrictionValue.to_list())
T014h = road_node.form_of_road_node.MustBeOfValues(FormOfRoadNodeValue.to_list())
T014i = road_service_point.type.MustBeOfValues(RoadServiceTypeValue.to_list())
T014j = road_service_area.type.MustBeOfValues(RoadServiceTypeValue.to_list())
T014k = railway_link.type.MustBeOfValues(RailwayTypeValue.to_list())
T014l = railway_link.electrified.MustBeOfValues(ElectrifiedValue.to_list())
T014m = railway_station_point.railway_use.MustBeOfValues(RailwayStationUseValue.to_list())
T014n = railway_station_area.railway_use.MustBeOfValues(RailwayStationUseValue.to_list())
T014o = aerodrome_point.aerodrome_category.MustBeOfValues(AerodromeCategoryValue.to_list())
T014p = aerodrome_area.aerodrome_category.MustBeOfValues(AerodromeCategoryValue.to_list())
T014q = aerodrome_point.aerodrome_type.MustBeOfValues(AerodromeTypeValue.to_list())
T014r = aerodrome_area.aerodrome_type.MustBeOfValues(AerodromeTypeValue.to_list())
T014s = aerodrome_point.use_restriction.MustBeOfValues(UseRestrictionValue.to_list())
T014t = aerodrome_area.use_restriction.MustBeOfValues(UseRestrictionValue.to_list())
T014u = runway_line.surface_composition.MustBeOfValues(SurfaceCategoryValue.to_list())
T014v = runway_area.surface_composition.MustBeOfValues(SurfaceCategoryValue.to_list())
T014w = ferry_crossing.ferry_use.MustBeOfValues(FerryUseValue.to_list())
T014x = ferry_crossing.tent_network.MustBeOfValues(TENTNetworkValue.to_list())
T014y = port_point.tent_network.MustBeOfValues(TENTNetworkValue.to_list())
T014z = port_area.tent_network.MustBeOfValues(TENTNetworkValue.to_list())

#endregion

#endregion

end_theme()

