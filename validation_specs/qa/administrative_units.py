from vrailang import *

begin_theme('ADMIN')

#region Featuretypes

DV1 = validation_specs = ValidationSpecification.ALL_SPECIFICATIONS['DV1']
administrative_unit_area_1 = DV1.theme('ADMIN').featureclass('administrative_unit_area_1')
administrative_unit_area_2 = DV1.theme('ADMIN').featureclass('administrative_unit_area_2')
administrative_unit_area_3 = DV1.theme('ADMIN').featureclass('administrative_unit_area_3')
administrative_unit_area_4 = DV1.theme('ADMIN').featureclass('administrative_unit_area_4')
administrative_unit_area_5 = DV1.theme('ADMIN').featureclass('administrative_unit_area_5')
administrative_unit_area_6 = DV1.theme('ADMIN').featureclass('administrative_unit_area_6')
residence_of_authority = DV1.theme('ADMIN').featureclass('residence_of_authority')
maritime_zone = DV1.theme('ADMIN').featureclass('maritime_zone')

#endregion


#region Validation checks

A001a = administrative_unit_area_1.DetermineFeatureCount().TreatAsStatistic()
A001b = administrative_unit_area_2.DetermineFeatureCount().TreatAsStatistic()
A001c = administrative_unit_area_3.DetermineFeatureCount().TreatAsStatistic()
A001d = administrative_unit_area_4.DetermineFeatureCount().TreatAsStatistic()
A001e = administrative_unit_area_5.DetermineFeatureCount().TreatAsStatistic()
A001f = administrative_unit_area_6.DetermineFeatureCount().TreatAsStatistic()
A001g = residence_of_authority.DetermineFeatureCount().TreatAsStatistic()
A001h = maritime_zone.DetermineFeatureCount().TreatAsStatistic()

A002a = administrative_unit_area_1.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002b = administrative_unit_area_2.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002c = administrative_unit_area_3.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002d = administrative_unit_area_4.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002e = administrative_unit_area_5.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002f = administrative_unit_area_6.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002g = residence_of_authority.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()
A002h = maritime_zone.DetermineFeatureCount(group_by_field_1='country').TreatAsStatistic()

A003a = administrative_unit_area_1.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003b = administrative_unit_area_2.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003c = administrative_unit_area_3.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003d = administrative_unit_area_4.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003e = administrative_unit_area_5.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003f = administrative_unit_area_6.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='land_cover_type')
A003g = maritime_zone.DetermineFeatureCount(group_by_field_1='country', group_by_field_2='zone_type')

A010a = administrative_unit_area_1.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010b = administrative_unit_area_2.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010c = administrative_unit_area_3.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010d = administrative_unit_area_4.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010e = administrative_unit_area_5.land_cover_type.DetermineCompletionRate().TreatAsStatistic()
A010f = administrative_unit_area_6.land_cover_type.DetermineCompletionRate().TreatAsStatistic()


#endregion

end_theme()
