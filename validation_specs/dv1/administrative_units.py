from vrailang import *
from validation_specs.domains import LandCoverTypeValue, MaritimeZoneTypeValue

begin_theme('ADMIN', 'au')

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
    w_step: integer
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: integer

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
    w_step: integer
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: integer

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
    w_step: integer
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: integer

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
    w_step: integer
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: integer

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
    w_step: integer
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: integer

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
    w_step: integer
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: integer


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
    w_step: integer
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: integer


class residence_of_authority(feature):
    objectid: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: PointZ[srid(3035)]
    name: jsonb
    label: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: integer
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: integer


# General content
#T001 = administrative_unit_area_1.MustComplyWithDataschema()


# # Geometric resolution

T001 = administrative_unit_area_1.geom.MustHaveCorrectGeometryType()
T002 = administrative_unit_area_2.geom.MustHaveCorrectGeometryType()
T003 = administrative_unit_area_3.geom.MustHaveCorrectGeometryType()
T004 = administrative_unit_area_4.geom.MustHaveCorrectGeometryType()
T005 = administrative_unit_area_5.geom.MustHaveCorrectGeometryType()
T006 = administrative_unit_area_6.geom.MustHaveCorrectGeometryType()

T007 = residence_of_authority.geom.MustHaveCorrectGeometryType()
T008 = maritime_zone.geom.MustHaveCorrectGeometryType()

# Data model and attribute resolution
# A020 = administrative_unit_area_1.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
# A021 = administrative_unit_area_2.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
# A022 = administrative_unit_area_3.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
# A023 = administrative_unit_area_4.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
# A024 = administrative_unit_area_5.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
# A025 = administrative_unit_area_6.land_cover_type.MustBeOfValues(LandCoverTypeValue.to_list())
# A026 = maritime_zone.zone_type.MustBeOfValues(MaritimeZoneTypeValue)

end_theme()
