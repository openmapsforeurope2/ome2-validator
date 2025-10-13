from vrailang import *

from validation_specs.dv1 import hydrography

begin_theme('HYDRO', 'hy')

fictitious_axis = hydrography.watercourse_link.filtered('"fictitious" = \'true\'')

#region Validation checks

H001a = hydrography.watercourse_link.DetermineFeatureCount().TreatAsStatistic()
H001b = hydrography.watercourse.DetermineFeatureCount().TreatAsStatistic()
H001c = hydrography.hydro_node.DetermineFeatureCount().TreatAsStatistic()
H001d = hydrography.dam_area.DetermineFeatureCount().TreatAsStatistic()
H001e = hydrography.dam_line.DetermineFeatureCount().TreatAsStatistic()
H001f = hydrography.dam_point.DetermineFeatureCount().TreatAsStatistic()
H001g = hydrography.falls_area.DetermineFeatureCount().TreatAsStatistic()
H001h = hydrography.falls_line.DetermineFeatureCount().TreatAsStatistic()
H001i = hydrography.falls_point.DetermineFeatureCount().TreatAsStatistic()
H001j = hydrography.lock_area.DetermineFeatureCount().TreatAsStatistic()
H001k = hydrography.lock_line.DetermineFeatureCount().TreatAsStatistic()
H001l = hydrography.lock_point.DetermineFeatureCount().TreatAsStatistic()
H001m = hydrography.watercourse_area.DetermineFeatureCount().TreatAsStatistic()
H001n = hydrography.standing_water.DetermineFeatureCount().TreatAsStatistic()
H001o = hydrography.shoreline.DetermineFeatureCount().TreatAsStatistic()
H001p = hydrography.shore.DetermineFeatureCount().TreatAsStatistic()
H001q = hydrography.drainage_basin.DetermineFeatureCount().TreatAsStatistic()

H002a = hydrography.watercourse_link.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002b = hydrography.watercourse.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002c = hydrography.hydro_node.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002d = hydrography.dam_area.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002e = hydrography.dam_line.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002f = hydrography.dam_point.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002g = hydrography.falls_area.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002h = hydrography.falls_line.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002i = hydrography.falls_point.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002j = hydrography.lock_area.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002k = hydrography.lock_line.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002l = hydrography.lock_point.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002m = hydrography.watercourse_area.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002n = hydrography.standing_water.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002o = hydrography.shoreline.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002p = hydrography.shore.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
H002q = hydrography.drainage_basin.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()

H003a = hydrography.fictitious_axis.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()

end_theme()
