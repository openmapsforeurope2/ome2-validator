from vrailang import *
from validation_specs.domains import *
from validation_specs.extents import Epsg3035Bounds

from validation_specs.dv1 import administrative_units

begin_theme('TRANS', 'tn')

#region Featuretypes

class road_link(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
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
    speed_limit: varchar[length(255)]
    condition_of_facility: varchar[length(255)]
    link_to_road: varchar[length(255)]
    national_road_code: varchar[length(255)]
    european_route_number: varchar[length(255)]
    road_name: jsonb
    road_label: varchar[length(255)]

class road_node(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: PointZ[srid(3035)]
    local_name: varchar[length(255)]
    form_of_road_node: varchar[length(255)]
    label: varchar[length(255)]

class road_service_area(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: MultiPolygonZ[srid(3035)]
    type: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]

class road_service_point(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: PointZ[srid(3035)]
    type: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]

class marker_post(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: PointZ[srid(3035)]
    link_to_road: varchar[length(255)]
    code: varchar[length(255)]
    distance: varchar[length(255)]
    w_link_to_national_road: varchar[length(255)]

class railway_link(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
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
    min_max_track: varchar[length(255)]
    nominal_track_gauge: varchar[length(255)]
    track_gauge_category: varchar[length(255)]
    speed_class: varchar[length(255)]
    railway_use: varchar[length(255)]
    access_restriction: varchar[length(255)]

class railway_station_area(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: MultiPolygonZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    station_code: varchar[length(255)]
    railway_use: varchar[length(255)]
    form_of_railway_station: varchar[length(255)]

class railway_station_point(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: PointZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    station_code: varchar[length(255)]
    railway_use: varchar[length(255)]
    form_of_railway_station: varchar[length(255)]

class aerodrome_point(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: PointZ[srid(3035)]
    designator_iata: varchar[length(255)]
    location_indicator_icao: varchar[length(255)]
    un_locode: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    aerodrome_category: varchar[length(255)]
    aerodrome_type: varchar[length(255)]
    use_restriction: varchar[length(255)]
    condition_of_facility: varchar[length(255)]

class aerodrome_area(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: MultiPolygonZ[srid(3035)]
    designator_iata: varchar[length(255)]
    location_indicator_icao: varchar[length(255)]
    un_locode: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    aerodrome_category: varchar[length(255)]
    aerodrome_type: varchar[length(255)]
    use_restriction: varchar[length(255)]
    condition_of_facility: varchar[length(255)]

class runway_area(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: MultiPolygonZ[srid(3035)]
    surface_composition: varchar[length(255)]

class ferry_crossing(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: MultiLineStringZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    ferry_use: varchar[length(255)]
    tent_network: varchar[length(255)]
    access_restriction: varchar[length(255)]

class port_area(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: MultiPolygonZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    un_locode: varchar[length(255)]
    tent_network: varchar[length(255)]

class port_point(feature):
    objectid: uuid[primary_key, notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    w_national_identifier: varchar[length(255)]
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4
    geom: PointZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    un_locode: varchar[length(255)]
    tent_network: varchar[length(255)]

#endregion

#region Derived featureclasses
motorway = road_link.filtered('"form_of_way" = \'motorway\'')
#endregion

#endregion

#region Validation checks

#region General content

T001a = road_link.MustComplyWithDataschema()
T001c = road_node.MustComplyWithDataschema()
T001d = road_service_area.MustComplyWithDataschema()
T001e = road_service_point.MustComplyWithDataschema()
T001f = marker_post.MustComplyWithDataschema()
T001g = railway_link.MustComplyWithDataschema()
T001i = railway_station_area.MustComplyWithDataschema()
T001j = railway_station_point.MustComplyWithDataschema()
T001k = aerodrome_area.MustComplyWithDataschema()
T001l = aerodrome_point.MustComplyWithDataschema()
T001m = runway_area.MustComplyWithDataschema()
T001o = ferry_crossing.MustComplyWithDataschema()
T001p = port_area.MustComplyWithDataschema()
T001q = port_point.MustComplyWithDataschema()

#endregion

# region Geometric resolution
T002a = road_link.geom.MustHaveCorrectCRS()
T002c = road_node.geom.MustHaveCorrectCRS()
T002d = road_service_area.geom.MustHaveCorrectCRS()
T002e = road_service_point.geom.MustHaveCorrectCRS()
T002f = marker_post.geom.MustHaveCorrectCRS()
T002g = railway_link.geom.MustHaveCorrectCRS()
T002i = railway_station_area.geom.MustHaveCorrectCRS()
T002j = railway_station_point.geom.MustHaveCorrectCRS()
T002k = aerodrome_area.geom.MustHaveCorrectCRS()
T002l = aerodrome_point.geom.MustHaveCorrectCRS()
T002m = runway_area.geom.MustHaveCorrectCRS()
T002o = ferry_crossing.geom.MustHaveCorrectCRS()
T002p = port_area.geom.MustHaveCorrectCRS()
T002q = port_point.geom.MustHaveCorrectCRS()


T003a = road_link.geom.MustHaveCorrectGeometryType()
T003c = road_node.geom.MustHaveCorrectGeometryType()
T003d = road_service_area.geom.MustHaveCorrectGeometryType()
T003e = road_service_point.geom.MustHaveCorrectGeometryType()
T003f = marker_post.geom.MustHaveCorrectGeometryType()
T003g = railway_link.geom.MustHaveCorrectGeometryType()
T003i = railway_station_area.geom.MustHaveCorrectGeometryType()
T003j = railway_station_point.geom.MustHaveCorrectGeometryType()
T003k = aerodrome_area.geom.MustHaveCorrectGeometryType()
T003l = aerodrome_point.geom.MustHaveCorrectGeometryType()
T003m = runway_area.geom.MustHaveCorrectGeometryType()
T003o = ferry_crossing.geom.MustHaveCorrectGeometryType()
T003p = port_area.geom.MustHaveCorrectGeometryType()
T003q = port_point.geom.MustHaveCorrectGeometryType()

T004a = road_link.MustHaveValidGeometry()
T004c = road_node.MustHaveValidGeometry()
T004d = road_service_area.MustHaveValidGeometry()
T004e = road_service_point.MustHaveValidGeometry()
T004f = marker_post.MustHaveValidGeometry()
T004g = railway_link.MustHaveValidGeometry()
T004i = railway_station_area.MustHaveValidGeometry()
T004j = railway_station_point.MustHaveValidGeometry()
T004k = aerodrome_area.MustHaveValidGeometry()
T004l = aerodrome_point.MustHaveValidGeometry()
T004m = runway_area.MustHaveValidGeometry()
T004o = ferry_crossing.MustHaveValidGeometry()
T004p = port_area.MustHaveValidGeometry()
T004q = port_point.MustHaveValidGeometry()

T005a = road_link.MustBeWithinExtent(Epsg3035Bounds)
T005c = road_node.MustBeWithinExtent(Epsg3035Bounds)
T005d = road_service_area.MustBeWithinExtent(Epsg3035Bounds)
T005e = road_service_point.MustBeWithinExtent(Epsg3035Bounds)
T005f = marker_post.MustBeWithinExtent(Epsg3035Bounds)
T005g = railway_link.MustBeWithinExtent(Epsg3035Bounds)
T005i = railway_station_area.MustBeWithinExtent(Epsg3035Bounds)
T005j = railway_station_point.MustBeWithinExtent(Epsg3035Bounds)
T005k = aerodrome_area.MustBeWithinExtent(Epsg3035Bounds)
T005l = aerodrome_point.MustBeWithinExtent(Epsg3035Bounds)
T005m = runway_area.MustBeWithinExtent(Epsg3035Bounds)
T005o = ferry_crossing.MustBeWithinExtent(Epsg3035Bounds)
T005p = port_area.MustBeWithinExtent(Epsg3035Bounds)
T005q = port_point.MustBeWithinExtent(Epsg3035Bounds)


T006a = road_link.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()
T006c = railway_link.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()
T006f = ferry_crossing.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()

T007a = aerodrome_area.AreaMustBeAtLeast(60000).TreatAsWarning()
T007b = port_area.AreaMustBeAtLeast(60000).TreatAsWarning()
T007c = railway_station_area.AreaMustBeAtLeast(60000).TreatAsWarning()
T007d = road_service_area.AreaMustBeAtLeast(60000).TreatAsWarning()
T007e = runway_area.AreaMustBeAtLeast(60000).TreatAsWarning()

#endregion

#region Data model and attribute resolution
T011a = road_link.objectid.MustNotBeNull()
T011c = road_node.objectid.MustNotBeNull()
T011d = road_service_area.objectid.MustNotBeNull()
T011e = road_service_point.objectid.MustNotBeNull()
T011f = marker_post.objectid.MustNotBeNull()
T011g = railway_link.objectid.MustNotBeNull()
T011i = railway_station_area.objectid.MustNotBeNull()
T011j = railway_station_point.objectid.MustNotBeNull()
T011k = aerodrome_area.objectid.MustNotBeNull()
T011l = aerodrome_point.objectid.MustNotBeNull()
T011m = runway_area.objectid.MustNotBeNull()
T011o = ferry_crossing.objectid.MustNotBeNull()
T011p = port_area.objectid.MustNotBeNull()
T011q = port_point.objectid.MustNotBeNull()

# TODO checks on road_link are very slow
T015a = road_link.form_of_way.MustBeOfValues(FormOfWayValue, separator='#')
T015b = road_link.functional_road_class.MustBeOfValues(FunctionalRoadClass, separator='#')
T015c = road_link.vertical_position.MustBeOfValues(VerticalPositionValue, separator='#')
T015d = road_link.road_surface_category.MustBeOfValues(RoadSurfaceCategoryValue, separator='#')
T015e = road_link.tent_network.MustBeOfValues(TENTNetworkValue, separator='#')
T015f = road_link.traffic_flow_direction.MustBeOfValues(LinkDirectionValue, separator='#')
T015g = road_link.access_restriction.MustBeOfValues(AccessRestrictionValue, separator='#')
T015h = road_node.form_of_road_node.MustBeOfValues(FormOfRoadNodeValue, separator='#')
T015i = road_service_point.type.MustBeOfValues(RoadServiceTypeValue, separator='#')
T015j = road_service_area.type.MustBeOfValues(RoadServiceTypeValue, separator='#')
T015k = railway_link.type.MustBeOfValues(RailwayTypeValue, separator='#')
T015l = railway_link.electrified.MustBeOfValues(ElectrifiedValue, separator='#')
T015m = railway_station_point.railway_use.MustBeOfValues(RailwayStationUseValue, separator='#')
T015n = railway_station_area.railway_use.MustBeOfValues(RailwayStationUseValue, separator='#')
T015o = aerodrome_point.aerodrome_category.MustBeOfValues(AerodromeCategoryValue, separator='#')
T015p = aerodrome_area.aerodrome_category.MustBeOfValues(AerodromeCategoryValue, separator='#')
T015q = aerodrome_point.aerodrome_type.MustBeOfValues(AerodromeTypeValue, separator='#')
T015r = aerodrome_area.aerodrome_type.MustBeOfValues(AerodromeTypeValue, separator='#')
T015s = aerodrome_point.use_restriction.MustBeOfValues(UseRestrictionValue, separator='#')
T015t = aerodrome_area.use_restriction.MustBeOfValues(UseRestrictionValue, separator='#')
T015v = runway_area.surface_composition.MustBeOfValues(SurfaceCategoryValue, separator='#')
T015w = ferry_crossing.ferry_use.MustBeOfValues(FerryUseValue, separator='#')
T015x = ferry_crossing.tent_network.MustBeOfValues(TENTNetworkValue, separator='#')
T015y = port_point.tent_network.MustBeOfValues(TENTNetworkValue, separator='#')
T015z = port_area.tent_network.MustBeOfValues(TENTNetworkValue, separator='#')

#endregion


#region Topology

T023_BUFFER = 10 # meter
T023_SIMPLIFY = 10 # meter
T023a = road_link.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country', 
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023c = road_node.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023d = road_service_area.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023e = road_service_point.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023f = marker_post.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023g = railway_link.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023i = railway_station_area.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023j = railway_station_point.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023k = aerodrome_area.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023l = aerodrome_point.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023m = runway_area.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023o = port_area.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)
T023p = port_point.MustBeInsideMatchingArea(
                            administrative_units.administrative_unit_area_1, id_field='country',
                            attribute_mapping=administrative_units.au2_to_au1_countries,
                            buffer=T023_BUFFER, simplify = T023_SIMPLIFY)

T024a = motorway.MustNotHaveDangles()

T025a = aerodrome_area.MustNotOverlapWithFeaturesOfSameType(['aerodrome_category', 'aerodrome_type'])
T025b = railway_station_area.MustNotOverlapWithFeaturesOfSameType(['railway_use'])
T025c = road_service_area.MustNotOverlapWithFeaturesOfSameType(['type'])
T025d = runway_area.MustNotOverlapWithFeaturesOfSameType(['surface_composition'])

#endregion

#region Edge matching

T031h = railway_link.MustBeConsistentAcrossBorder(administrative_units.administrative_unit_area_1, ["type", "condition_of_facility"])

#endregion

T032a = aerodrome_area.AdjacentFacesMustDiffer(['country', 'label', 'aerodrome_category', 'aerodrome_type', 'use_restriction', 'designator_iata', 'location_indicator_icao', 'un_locode'])
T032b = port_area.AdjacentFacesMustDiffer(['country', 'label', 'un_locode', 'tent_network'])
T032c = road_service_area.AdjacentFacesMustDiffer(['country', 'label', 'type'])
T032d = railway_station_area.AdjacentFacesMustDiffer(['country', 'label', 'station_code', 'railway_use', 'form_of_railway_station'])
T032e = runway_area.AdjacentFacesMustDiffer(['country', 'surface_composition'])

T033a = aerodrome_area.MustBeSinglePart()
T033b = port_area.MustBeSinglePart()
T033c = road_link.MustBeSinglePart()
T033g = ferry_crossing.MustBeSinglePart()

T034a = road_link.MustNotHavePseudoNodes(attributes=['vertical_position', 'vertical_level', 'street_label'])
T034c = railway_link.MustNotHavePseudoNodes(attributes=['vertical_position', 'vertical_level', 'number_of_tracks', 'electrified'])
T034f = ferry_crossing.MustNotHavePseudoNodes()

#endregion

end_theme()
