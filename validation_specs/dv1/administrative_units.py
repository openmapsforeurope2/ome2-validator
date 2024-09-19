from vrailang import *
from validation_specs.domains import LandCoverTypeValue, MaritimeZoneTypeValue, CountryCodeValue
from validation_specs.extents import Epsg3035Bounds

begin_theme('ADMIN', 'au')

#region Featuretypes

#region Administrative units

class administrative_unit_area_1(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygon[srid(3035)]
    national_code: varchar[length(255)]
    shn: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    national_level_code: varchar[length(255)]
    link_to_residence_of_authority: varchar[length(255)]
    land_cover_type: varchar[length(255)]
    valid_from: timestamp
    valid_to: timestamp
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class administrative_unit_area_2(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygon[srid(3035)]
    national_code: varchar[length(255)]
    shn: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    national_level_code: varchar[length(255)]
    link_to_residence_of_authority: varchar[length(255)]
    land_cover_type: varchar[length(255)]
    valid_from: timestamp
    valid_to: timestamp
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class administrative_unit_area_3(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygon[srid(3035)]
    national_code: varchar[length(255)]
    shn: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    national_level_code: varchar[length(255)]
    link_to_residence_of_authority: varchar[length(255)]
    land_cover_type: varchar[length(255)]
    valid_from: timestamp
    valid_to: timestamp
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class administrative_unit_area_4(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygon[srid(3035)]
    national_code: varchar[length(255)]
    shn: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    national_level_code: varchar[length(255)]
    link_to_residence_of_authority: varchar[length(255)]
    land_cover_type: varchar[length(255)]
    valid_from: timestamp
    valid_to: timestamp
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class administrative_unit_area_5(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygon[srid(3035)]
    national_code: varchar[length(255)]
    shn: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    national_level_code: varchar[length(255)]
    link_to_residence_of_authority: varchar[length(255)]
    land_cover_type: varchar[length(255)]
    valid_from: timestamp
    valid_to: timestamp
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

class administrative_unit_area_6(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygon[srid(3035)]
    national_code: varchar[length(255)]
    shn: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    national_level_code: varchar[length(255)]
    link_to_residence_of_authority: varchar[length(255)]
    land_cover_type: varchar[length(255)]
    valid_from: timestamp
    valid_to: timestamp
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

#endregion


#region Residence of authority

class residence_of_authority(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: int4
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: int4

#endregion


#region Maritime Units

class maritime_zone(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: MultiPolygon[srid(3035)]
    national_code: varchar[length(255)]
    shn: varchar[length(255)]
    name: jsonb
    label: varchar[length(255)]
    national_level_code: varchar[length(255)]
    zone_type: varchar[length(255)]
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
A001a = administrative_unit_area_1.MustComplyWithDataschema()
A001b = administrative_unit_area_2.MustComplyWithDataschema()
A001c = administrative_unit_area_3.MustComplyWithDataschema()
A001d = administrative_unit_area_4.MustComplyWithDataschema()
A001e = administrative_unit_area_5.MustComplyWithDataschema()
A001f = administrative_unit_area_6.MustComplyWithDataschema()
A001g = maritime_zone.MustComplyWithDataschema()
A001h = residence_of_authority.MustComplyWithDataschema()

#endregion

#region Geometric resolution

A002a = administrative_unit_area_1.geom.MustHaveCorrectCRS()
A002b = administrative_unit_area_2.geom.MustHaveCorrectCRS()
A002c = administrative_unit_area_3.geom.MustHaveCorrectCRS()
A002d = administrative_unit_area_4.geom.MustHaveCorrectCRS()
A002e = administrative_unit_area_5.geom.MustHaveCorrectCRS()
A002f = administrative_unit_area_6.geom.MustHaveCorrectCRS()
A002g = maritime_zone.geom.MustHaveCorrectCRS()
A002h = residence_of_authority.geom.MustHaveCorrectCRS()

A003a = administrative_unit_area_1.geom.MustHaveCorrectGeometryType()
A003b = administrative_unit_area_2.geom.MustHaveCorrectGeometryType()
A003c = administrative_unit_area_3.geom.MustHaveCorrectGeometryType()
A003d = administrative_unit_area_4.geom.MustHaveCorrectGeometryType()
A003e = administrative_unit_area_5.geom.MustHaveCorrectGeometryType()
A003f = administrative_unit_area_6.geom.MustHaveCorrectGeometryType()
A003g = residence_of_authority.geom.MustHaveCorrectGeometryType()
A003h = maritime_zone.geom.MustHaveCorrectGeometryType()

A004a = administrative_unit_area_1.MustHaveValidGeometry()
A004b = administrative_unit_area_2.MustHaveValidGeometry()
A004c = administrative_unit_area_3.MustHaveValidGeometry()
A004d = administrative_unit_area_4.MustHaveValidGeometry()
A004e = administrative_unit_area_5.MustHaveValidGeometry()
A004f = administrative_unit_area_6.MustHaveValidGeometry()
A004g = maritime_zone.MustHaveValidGeometry()
A004h = residence_of_authority.MustHaveValidGeometry()

A005a = administrative_unit_area_1.MustBeWithinExtent(Epsg3035Bounds)
A005b = administrative_unit_area_2.MustBeWithinExtent(Epsg3035Bounds)
A005c = administrative_unit_area_3.MustBeWithinExtent(Epsg3035Bounds)
A005d = administrative_unit_area_4.MustBeWithinExtent(Epsg3035Bounds)
A005e = administrative_unit_area_5.MustBeWithinExtent(Epsg3035Bounds)
A005f = administrative_unit_area_6.MustBeWithinExtent(Epsg3035Bounds)
A005g = maritime_zone.MustBeWithinExtent(Epsg3035Bounds)
A005h = residence_of_authority.MustBeWithinExtent(Epsg3035Bounds)


A006a = administrative_unit_area_1.AreaMustBeAtLeast(200_000_000)
A006b = administrative_unit_area_2.AreaMustBeAtLeast(20_000_000)
A006c = administrative_unit_area_3.AreaMustBeAtLeast(5_000_000)
A006d = administrative_unit_area_4.AreaMustBeAtLeast(25_000_000)
A006e = administrative_unit_area_5.AreaMustBeAtLeast(1_000_000)
A006f = administrative_unit_area_6.AreaMustBeAtLeast(25_000)
A006g = maritime_zone.AreaMustBeAtLeast(1_000_000_000)


A007a = administrative_unit_area_1.VerticesDistanceMustBeAtLeast(0.05)
A007b = administrative_unit_area_2.VerticesDistanceMustBeAtLeast(0.05)
A007c = administrative_unit_area_3.VerticesDistanceMustBeAtLeast(0.05)
A007d = administrative_unit_area_4.VerticesDistanceMustBeAtLeast(0.05)
A007e = administrative_unit_area_5.VerticesDistanceMustBeAtLeast(0.05)
A007f = administrative_unit_area_6.VerticesDistanceMustBeAtLeast(0.05)
A007g = maritime_zone.VerticesDistanceMustBeAtLeast(0.05)
A007h = residence_of_authority.VerticesDistanceMustBeAtLeast(0.05)

#endregion

#region Data model and attribute resolution

A014a = administrative_unit_area_1.country.MustBeOfValues(CountryCodeValue)
A014b = administrative_unit_area_2.country.MustBeOfValues(CountryCodeValue)
A014c = administrative_unit_area_3.country.MustBeOfValues(CountryCodeValue)
A014d = administrative_unit_area_4.country.MustBeOfValues(CountryCodeValue)
A014e = administrative_unit_area_5.country.MustBeOfValues(CountryCodeValue)
A014f = administrative_unit_area_6.country.MustBeOfValues(CountryCodeValue)
A014g = maritime_zone.country.MustBeOfValues(CountryCodeValue)
A014h = residence_of_authority.country.MustBeOfValues(CountryCodeValue)

A015a = administrative_unit_area_1.land_cover_type.MustBeOfValues(LandCoverTypeValue)
A015b = administrative_unit_area_2.land_cover_type.MustBeOfValues(LandCoverTypeValue)
A015c = administrative_unit_area_3.land_cover_type.MustBeOfValues(LandCoverTypeValue)
A015d = administrative_unit_area_4.land_cover_type.MustBeOfValues(LandCoverTypeValue)
A015e = administrative_unit_area_5.land_cover_type.MustBeOfValues(LandCoverTypeValue)
A015f = administrative_unit_area_6.land_cover_type.MustBeOfValues(LandCoverTypeValue)
A015g = maritime_zone.zone_type.MustBeOfValues(MaritimeZoneTypeValue)




#endregion

#region Topology
A023a = administrative_unit_area_2.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A023b = administrative_unit_area_3.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A023c = administrative_unit_area_4.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A023d = administrative_unit_area_5.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A023e = administrative_unit_area_6.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A023f = residence_of_authority.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')

A021a = administrative_unit_area_1.MustNotHaveGaps()
A021b = administrative_unit_area_2.MustNotHaveGaps()
A021c = administrative_unit_area_3.MustNotHaveGaps()
A021d = administrative_unit_area_4.MustNotHaveGaps()
A021e = administrative_unit_area_5.MustNotHaveGaps()
A021f = administrative_unit_area_6.MustNotHaveGaps()

A022a = administrative_unit_area_1.MustNotHaveOverlaps()
A022b = administrative_unit_area_2.MustNotHaveOverlaps()
A022c = administrative_unit_area_3.MustNotHaveOverlaps()
A022d = administrative_unit_area_4.MustNotHaveOverlaps()
A022e = administrative_unit_area_5.MustNotHaveOverlaps()
A022f = administrative_unit_area_6.MustNotHaveOverlaps()



#endregion

#region Statistics

A091a = administrative_unit_area_1.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A091b = administrative_unit_area_2.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A091c = administrative_unit_area_3.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A091d = administrative_unit_area_4.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A091e = administrative_unit_area_5.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A091f = administrative_unit_area_6.land_cover_type.CalculateCompletionRate().TreatAsStatistic()


#endregion

#endregion

end_theme()
