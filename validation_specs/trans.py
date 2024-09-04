from vrailang import *

begin_theme('TRANS', 'tn')

class runway_line(feature):
    object_id: uuid[notnull]
    country: varchar[length(8)]
    begin_lifespan_version: timestamp
    end_lifespan_version: timestamp
    geom: multilinestringz[srid(3035)]
    surface_composition: varchar[length(255)]
    w_national_identifier: varchar[length(255)]
    w_step: integer
    xy_source: varchar[length(255)]
    z_source: varchar[length(255)]
    w_scale: varchar[length(80)]
    w_release: integer

T001 = runway_line.LengthMustBeAtLeast(1000, check_multilines_per_linestring=False).TreatAsWarning()
T001a = runway_line.LengthMustBeAtLeast(1000, check_multilines_per_linestring=False)
T042 = runway_line.object_id.MustNotBeNull()


end_theme()
