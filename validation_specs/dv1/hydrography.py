from vrailang import *
from validation_specs.domains import *
from validation_specs.extents import Epsg3035Bounds

from validation_specs.dv1 import administrative_units

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


# class glacier_snowfield(feature):
#     objectid: uuid[notnull]
#     country: varchar[length(8)]
#     begin_lifespan_version: timestamp
#     end_lifespan_version: timestamp
#     geom: MultiPolygonZ[srid(3035)]
#     ice_area_type: varchar[length(255)]
#     name: jsonb
#     label: varchar[length(255)]


# class shoreline_construction_area(feature):
#     objectid: uuid[notnull]
#     country: varchar[length(8)]
#     begin_lifespan_version: timestamp
#     end_lifespan_version: timestamp
#     geom: MultiPolygonZ[srid(3035)]
#     shoreline_construction_type: varchar[length(255)]
#     name: jsonb
#     label: varchar[length(255)]


# class shoreline_construction_line(feature):
#     objectid: uuid[notnull]
#     country: varchar[length(8)]
#     begin_lifespan_version: timestamp
#     end_lifespan_version: timestamp
#     geom: LineStringZ[srid(3035)]
#     shoreline_construction_type: varchar[length(255)]
#     name: jsonb
#     label: varchar[length(255)]


# class wetland(feature):
#     objectid: uuid[notnull]
#     country: varchar[length(8)]
#     begin_lifespan_version: timestamp
#     end_lifespan_version: timestamp
#     geom: MultiPolygonZ[srid(3035)]
#     local_name: varchar[length(255)]
#     tidal: varchar[length(255)]

#endregion

#endregion


#region Validation checks

#region General content

H001a = watercourse_link.MustComplyWithDataschema()
H001b = watercourse.MustComplyWithDataschema()
H001c = hydro_node.MustComplyWithDataschema()
H001d = dam_area.MustComplyWithDataschema()
H001e = dam_line.MustComplyWithDataschema()
H001f = dam_point.MustComplyWithDataschema()
H001g = falls_area.MustComplyWithDataschema()
H001h = falls_line.MustComplyWithDataschema()
H001i = falls_point.MustComplyWithDataschema()
H001j = lock_area.MustComplyWithDataschema()
H001k = lock_line.MustComplyWithDataschema()
H001l = lock_point.MustComplyWithDataschema()
H001m = watercourse_area.MustComplyWithDataschema()
H001n = standing_water.MustComplyWithDataschema()
H001o = shoreline.MustComplyWithDataschema()
H001p = shore.MustComplyWithDataschema()
H001q = drainage_basin.MustComplyWithDataschema()
# H001r = glacier_snowfield.MustComplyWithDataschema()
# H001s = shoreline_construction_area.MustComplyWithDataschema()
# H001t = shoreline_construction_line.MustComplyWithDataschema()
# H001u = wetland.MustComplyWithDataschema()

#endregion

#region Geometric resolution

H002a = watercourse_link.geom.MustHaveCorrectCRS()
H002b = watercourse.geom.MustHaveCorrectCRS()
H002c = hydro_node.geom.MustHaveCorrectCRS()
H002d = dam_area.geom.MustHaveCorrectCRS()
H002e = dam_line.geom.MustHaveCorrectCRS()
H002f = dam_point.geom.MustHaveCorrectCRS()
H002g = falls_area.geom.MustHaveCorrectCRS()
H002h = falls_line.geom.MustHaveCorrectCRS()
H002i = falls_point.geom.MustHaveCorrectCRS()
H002j = lock_area.geom.MustHaveCorrectCRS()
H002k = lock_line.geom.MustHaveCorrectCRS()
H002l = lock_point.geom.MustHaveCorrectCRS()
H002m = watercourse_area.geom.MustHaveCorrectCRS()
H002n = standing_water.geom.MustHaveCorrectCRS()
H002o = shoreline.geom.MustHaveCorrectCRS()
H002p = shore.geom.MustHaveCorrectCRS()
H002q = drainage_basin.geom.MustHaveCorrectCRS()
# H002r = glacier_snowfield.geom.MustHaveCorrectCRS()
# H002s = shoreline_construction_area.geom.MustHaveCorrectCRS()
# H002t = shoreline_construction_line.geom.MustHaveCorrectCRS()
# H002u = wetland.geom.MustHaveCorrectCRS()

H003a = watercourse_link.geom.MustHaveCorrectGeometryType()
H003b = watercourse.geom.MustHaveCorrectGeometryType()
H003c = hydro_node.geom.MustHaveCorrectGeometryType()
H003d = dam_area.geom.MustHaveCorrectGeometryType()
H003e = dam_line.geom.MustHaveCorrectGeometryType()
H003f = dam_point.geom.MustHaveCorrectGeometryType()
H003g = falls_area.geom.MustHaveCorrectGeometryType()
H003h = falls_line.geom.MustHaveCorrectGeometryType()
H003i = falls_point.geom.MustHaveCorrectGeometryType()
H003j = lock_area.geom.MustHaveCorrectGeometryType()
H003k = lock_line.geom.MustHaveCorrectGeometryType()
H003l = lock_point.geom.MustHaveCorrectGeometryType()
H003m = watercourse_area.geom.MustHaveCorrectGeometryType()
H003n = standing_water.geom.MustHaveCorrectGeometryType()
H003o = shoreline.geom.MustHaveCorrectGeometryType()
H003p = shore.geom.MustHaveCorrectGeometryType()
H003q = drainage_basin.geom.MustHaveCorrectGeometryType()
# H003r = glacier_snowfield.geom.MustHaveCorrectGeometryType()
# H003s = shoreline_construction_area.geom.MustHaveCorrectGeometryType()
# H003t = shoreline_construction_line.geom.MustHaveCorrectGeometryType()
# H003u = wetland.geom.MustHaveCorrectGeometryType()

H004a = watercourse_link.MustHaveValidGeometry()
H004b = watercourse.MustHaveValidGeometry()
H004c = hydro_node.MustHaveValidGeometry()
H004d = dam_area.MustHaveValidGeometry()
H004e = dam_line.MustHaveValidGeometry()
H004f = dam_point.MustHaveValidGeometry()
H004g = falls_area.MustHaveValidGeometry()
H004h = falls_line.MustHaveValidGeometry()
H004i = falls_point.MustHaveValidGeometry()
H004j = lock_area.MustHaveValidGeometry()
H004k = lock_line.MustHaveValidGeometry()
H004l = lock_point.MustHaveValidGeometry()
H004m = watercourse_area.MustHaveValidGeometry()
H004n = standing_water.MustHaveValidGeometry()
H004o = shoreline.MustHaveValidGeometry()
H004p = shore.MustHaveValidGeometry()
H004q = drainage_basin.MustHaveValidGeometry()
# H004r = glacier_snowfield.MustHaveValidGeometry()
# H004s = shoreline_construction_area.MustHaveValidGeometry()
# H004t = shoreline_construction_line.MustHaveValidGeometry()
# H004u = wetland.MustHaveValidGeometry()

H005a = watercourse_link.MustBeWithinExtent(Epsg3035Bounds)
H005b = watercourse.MustBeWithinExtent(Epsg3035Bounds)
H005c = hydro_node.MustBeWithinExtent(Epsg3035Bounds)
H005d = dam_area.MustBeWithinExtent(Epsg3035Bounds)
H005e = dam_line.MustBeWithinExtent(Epsg3035Bounds)
H005f = dam_point.MustBeWithinExtent(Epsg3035Bounds)
H005g = falls_area.MustBeWithinExtent(Epsg3035Bounds)
H005h = falls_line.MustBeWithinExtent(Epsg3035Bounds)
H005i = falls_point.MustBeWithinExtent(Epsg3035Bounds)
H005j = lock_area.MustBeWithinExtent(Epsg3035Bounds)
H005k = lock_line.MustBeWithinExtent(Epsg3035Bounds)
H005l = lock_point.MustBeWithinExtent(Epsg3035Bounds)
H005m = watercourse_area.MustBeWithinExtent(Epsg3035Bounds)
H005n = standing_water.MustBeWithinExtent(Epsg3035Bounds)
H005o = shoreline.MustBeWithinExtent(Epsg3035Bounds)
H005p = shore.MustBeWithinExtent(Epsg3035Bounds)
H005q = drainage_basin.MustBeWithinExtent(Epsg3035Bounds)
# H005r = glacier_snowfield.MustBeWithinExtent(Epsg3035Bounds)
# H005s = shoreline_construction_area.MustBeWithinExtent(Epsg3035Bounds)
# H005t = shoreline_construction_line.MustBeWithinExtent(Epsg3035Bounds)
# H005u = wetland.MustBeWithinExtent(Epsg3035Bounds)


H006a = dam_line.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()
H006b = falls_line.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()
H006c = lock_line.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()
H006d = shoreline.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()
H006e = watercourse_link.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()
H006f = watercourse.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()
H006g = drainage_basin.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()
# H006h = shoreline_construction_line.LengthMustBeAtLeast(100, check_multilines_per_linestring=False).TreatAsWarning()

#endregion


#region Data model and attribute resolution

H011a = watercourse_link.objectid.MustNotBeNull()
H011b = watercourse.objectid.MustNotBeNull()
H011c = hydro_node.objectid.MustNotBeNull()
H011d = dam_area.objectid.MustNotBeNull()
H011e = dam_line.objectid.MustNotBeNull()
H011f = dam_point.objectid.MustNotBeNull()
H011g = falls_area.objectid.MustNotBeNull()
H011h = falls_line.objectid.MustNotBeNull()
H011i = falls_point.objectid.MustNotBeNull()
H011j = lock_area.objectid.MustNotBeNull()
H011k = lock_line.objectid.MustNotBeNull()
H011l = lock_point.objectid.MustNotBeNull()
H011m = watercourse_area.objectid.MustNotBeNull()
H011n = standing_water.objectid.MustNotBeNull()
H011o = shoreline.objectid.MustNotBeNull()
H011p = shore.objectid.MustNotBeNull()
H011q = drainage_basin.objectid.MustNotBeNull()
# H011r = glacier_snowfield.objectid.MustNotBeNull()
# H011s = shoreline_construction_area.objectid.MustNotBeNull()
# H011t = shoreline_construction_line.objectid.MustNotBeNull()
# H011u = wetland.objectid.MustNotBeNull()

H014a = watercourse_link.country.MustBeOfValues(CountryCodeValue)
H014b = watercourse.country.MustBeOfValues(CountryCodeValue)
H014c = hydro_node.country.MustBeOfValues(CountryCodeValue)
H014d = dam_area.country.MustBeOfValues(CountryCodeValue)
H014e = dam_line.country.MustBeOfValues(CountryCodeValue)
H014f = dam_point.country.MustBeOfValues(CountryCodeValue)
H014g = falls_area.country.MustBeOfValues(CountryCodeValue)
H014h = falls_line.country.MustBeOfValues(CountryCodeValue)
H014i = falls_point.country.MustBeOfValues(CountryCodeValue)
H014j = lock_area.country.MustBeOfValues(CountryCodeValue)
H014k = lock_line.country.MustBeOfValues(CountryCodeValue)
H014l = lock_point.country.MustBeOfValues(CountryCodeValue)
H014m = watercourse_area.country.MustBeOfValues(CountryCodeValue)
H014n = standing_water.country.MustBeOfValues(CountryCodeValue)
H014o = shoreline.country.MustBeOfValues(CountryCodeValue)
H014p = shore.country.MustBeOfValues(CountryCodeValue)
H014q = drainage_basin.country.MustBeOfValues(CountryCodeValue)
# H014r = glacier_snowfield.country.MustBeOfValues(CountryCodeValue)
# H014s = shoreline_construction_area.country.MustBeOfValues(CountryCodeValue)
# H014t = shoreline_construction_line.country.MustBeOfValues(CountryCodeValue)
# H014u = wetland.country.MustBeOfValues(CountryCodeValue)

H015a = watercourse_link.level.MustBeOfValues(VerticalPositionValue)
H015b = watercourse_link.persistence.MustBeOfValues(HydrologicalPersistenceValue)
H015c = watercourse_link.flow_direction.MustBeOfValues(LinkDirectionValue)
H015d = watercourse_link.origin.MustBeOfValues(OriginValue)
H015e = watercourse_link.tent_network.MustBeOfValues(TENTNetworkValue)
H015f = watercourse_link.cemt_class.MustBeOfValues(CEMTClassValue)
H015g = hydro_node.hydro_node_category.MustBeOfValues(HydroNodeCategoryValue)
H015h = shore.composition.MustBeOfValues(ShoreTypeValue)
H015i = shoreline.water_level.MustBeOfValues(WaterLevelValue)
H015j = shoreline.origin.MustBeOfValues(OriginValue)
# H015k = shoreline_construction_area.shoreline_construction_type.MustBeOfValues(ShorelineConstructionTypeValue)
# H015l = shoreline_construction_line.shoreline_construction_type.MustBeOfValues(ShorelineConstructionTypeValue)
H015m = standing_water.persistence.MustBeOfValues(HydrologicalPersistenceValue)
H015n = standing_water.origin.MustBeOfValues(OriginValue)
H015o = watercourse_area.persistence.MustBeOfValues(HydrologicalPersistenceValue)
H015p = watercourse_area.origin.MustBeOfValues(OriginValue)

#endregion


#region Topology

H023a = watercourse_link.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023b = watercourse.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023c = hydro_node.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023d = dam_area.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023e = dam_line.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023f = dam_point.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023g = falls_area.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023h = falls_line.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023i = falls_point.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023j = lock_area.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023k = lock_line.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023l = lock_point.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023m = watercourse_area.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023n = standing_water.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023o = shore.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')
H023p = drainage_basin.MustBeInsideMatchingArea(administrative_units.administrative_unit_area_1, id_field='country')

#endregion


#endregion

end_theme()
