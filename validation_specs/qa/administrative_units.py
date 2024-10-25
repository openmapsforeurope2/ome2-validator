from vrailang import *

from validation_specs.dv1 import administrative_units

begin_theme('ADMIN')


#region Validation checks

A001a = administrative_units.administrative_unit_area_1.DetermineFeatureCount().TreatAsStatistic()
A001b = administrative_units.administrative_unit_area_2.DetermineFeatureCount().TreatAsStatistic()
A001c = administrative_units.administrative_unit_area_3.DetermineFeatureCount().TreatAsStatistic()
A001d = administrative_units.administrative_unit_area_4.DetermineFeatureCount().TreatAsStatistic()
A001e = administrative_units.administrative_unit_area_5.DetermineFeatureCount().TreatAsStatistic()
A001f = administrative_units.administrative_unit_area_6.DetermineFeatureCount().TreatAsStatistic()
A001g = administrative_units.residence_of_authority.DetermineFeatureCount().TreatAsStatistic()
A001h = administrative_units.maritime_zone.DetermineFeatureCount().TreatAsStatistic()

A002a = administrative_units.administrative_unit_area_1.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002b = administrative_units.administrative_unit_area_2.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002c = administrative_units.administrative_unit_area_3.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002d = administrative_units.administrative_unit_area_4.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002e = administrative_units.administrative_unit_area_5.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002f = administrative_units.administrative_unit_area_6.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002g = administrative_units.residence_of_authority.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002h = administrative_units.maritime_zone.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()

A003a = administrative_units.administrative_unit_area_1.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003b = administrative_units.administrative_unit_area_2.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003c = administrative_units.administrative_unit_area_3.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003d = administrative_units.administrative_unit_area_4.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003e = administrative_units.administrative_unit_area_5.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003f = administrative_units.administrative_unit_area_6.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003g = administrative_units.maritime_zone.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='zone_type')

A010a = administrative_units.administrative_unit_area_1.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010b = administrative_units.administrative_unit_area_2.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010c = administrative_units.administrative_unit_area_3.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010d = administrative_units.administrative_unit_area_4.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010e = administrative_units.administrative_unit_area_5.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010f = administrative_units.administrative_unit_area_6.land_cover_type.DetermineCompletionRate().TreatAsStatistic()


#endregion

end_theme()
