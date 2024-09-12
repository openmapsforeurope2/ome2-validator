from vrailang import *
from validation_specs.domains import LandCoverTypeValue, MaritimeZoneTypeValue, CountryCodeValue

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
A001 = administrative_unit_area_1.MustComplyWithDataschema()
A002 = administrative_unit_area_2.MustComplyWithDataschema()
A003 = administrative_unit_area_3.MustComplyWithDataschema()
A004 = administrative_unit_area_4.MustComplyWithDataschema()
A005 = administrative_unit_area_5.MustComplyWithDataschema()
A006 = administrative_unit_area_6.MustComplyWithDataschema()
A007 = maritime_zone.MustComplyWithDataschema()
A008 = residence_of_authority.MustComplyWithDataschema()

#endregion

#region Geometric resolution

A021 = administrative_unit_area_1.geom.MustHaveCorrectCRS()
A022 = administrative_unit_area_2.geom.MustHaveCorrectCRS()
A023 = administrative_unit_area_3.geom.MustHaveCorrectCRS()
A024 = administrative_unit_area_4.geom.MustHaveCorrectCRS()
A025 = administrative_unit_area_5.geom.MustHaveCorrectCRS()
A026 = administrative_unit_area_6.geom.MustHaveCorrectCRS()
A027 = maritime_zone.geom.MustHaveCorrectCRS()
A028 = residence_of_authority.geom.MustHaveCorrectCRS()

A011 = administrative_unit_area_1.geom.MustHaveCorrectGeometryType()
A012 = administrative_unit_area_2.geom.MustHaveCorrectGeometryType()
A013 = administrative_unit_area_3.geom.MustHaveCorrectGeometryType()
A014 = administrative_unit_area_4.geom.MustHaveCorrectGeometryType()
A015 = administrative_unit_area_5.geom.MustHaveCorrectGeometryType()
A016 = administrative_unit_area_6.geom.MustHaveCorrectGeometryType()
A017 = residence_of_authority.geom.MustHaveCorrectGeometryType()
A018 = maritime_zone.geom.MustHaveCorrectGeometryType()

A031 = administrative_unit_area_1.MustHaveValidGeometry()
A032 = administrative_unit_area_2.MustHaveValidGeometry()
A033 = administrative_unit_area_3.MustHaveValidGeometry()
A034 = administrative_unit_area_4.MustHaveValidGeometry()
A035 = administrative_unit_area_5.MustHaveValidGeometry()
A036 = administrative_unit_area_6.MustHaveValidGeometry()
A037 = maritime_zone.MustHaveValidGeometry()
A038 = residence_of_authority.MustHaveValidGeometry()


A051 = administrative_unit_area_1.AreaMustBeAtLeast(200_000_000)
A052 = administrative_unit_area_2.AreaMustBeAtLeast(20_000_000)
A053 = administrative_unit_area_3.AreaMustBeAtLeast(5_000_000)
A054 = administrative_unit_area_4.AreaMustBeAtLeast(25_000_000)
A055 = administrative_unit_area_5.AreaMustBeAtLeast(1_000_000)
A056 = administrative_unit_area_6.AreaMustBeAtLeast(25_000)
A057 = maritime_zone.AreaMustBeAtLeast(1_000_000_000)


A061 = administrative_unit_area_1.VerticesDistanceMustBeAtLeast(0.05)
A062 = administrative_unit_area_2.VerticesDistanceMustBeAtLeast(0.05)
A063 = administrative_unit_area_3.VerticesDistanceMustBeAtLeast(0.05)
A064 = administrative_unit_area_4.VerticesDistanceMustBeAtLeast(0.05)
A065 = administrative_unit_area_5.VerticesDistanceMustBeAtLeast(0.05)
A066 = administrative_unit_area_6.VerticesDistanceMustBeAtLeast(0.05)
A067 = maritime_zone.VerticesDistanceMustBeAtLeast(0.05)
A068 = residence_of_authority.VerticesDistanceMustBeAtLeast(0.05)

#endregion

#region Data model and attribute resolution
A020 = administrative_unit_area_1.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
A021 = administrative_unit_area_2.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
A022 = administrative_unit_area_3.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
A023 = administrative_unit_area_4.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
A024 = administrative_unit_area_5.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
A025 = administrative_unit_area_6.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
A026 = maritime_zone.zone_type.MustBeOfValues(MaritimeZoneTypeValue)

A051 = administrative_unit_area_1.country.MustBeOfValues(CountryCodeValue.to_list())
A052 = administrative_unit_area_2.country.MustBeOfValues(CountryCodeValue.to_list())
A053 = administrative_unit_area_3.country.MustBeOfValues(CountryCodeValue.to_list())
A054 = administrative_unit_area_4.country.MustBeOfValues(CountryCodeValue.to_list())
A055 = administrative_unit_area_5.country.MustBeOfValues(CountryCodeValue.to_list())
A056 = administrative_unit_area_6.country.MustBeOfValues(CountryCodeValue.to_list())
A057 = maritime_zone.country.MustBeOfValues(CountryCodeValue.to_list())
A058 = residence_of_authority.country.MustBeOfValues(CountryCodeValue.to_list())


#endregion

#region Topology
A042 = administrative_unit_area_2.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A043 = administrative_unit_area_3.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A044 = administrative_unit_area_4.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A045 = administrative_unit_area_5.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A046 = administrative_unit_area_6.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')
A047 = residence_of_authority.MustBeInsideMatchingArea(administrative_unit_area_1, id_field='country')

#endregion

#region Statistics

A091 = administrative_unit_area_1.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A092 = administrative_unit_area_2.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A093 = administrative_unit_area_3.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A094 = administrative_unit_area_4.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A095 = administrative_unit_area_5.land_cover_type.CalculateCompletionRate().TreatAsStatistic()
A096 = administrative_unit_area_6.land_cover_type.CalculateCompletionRate().TreatAsStatistic()


#endregion

#endregion

end_theme()
