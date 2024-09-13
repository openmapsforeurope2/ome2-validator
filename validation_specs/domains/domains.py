from enum import Enum

class DomainEnum(Enum):

    @classmethod
    def to_list(cls):
        return list(map(lambda x: x.value, cls))


class LandCoverTypeValue(DomainEnum):
    LAND_AREA = 'land_area'
    COASTAL_WATER = 'coastal_water'
    INLAND_WATER = 'inland_water'
    IN_DISPUTE_AREA = 'in_dispute_area'
    VOID_UNK = 'void_unk'


class MaritimeZoneTypeValue(DomainEnum):
    INTERNAL_WATERS = 'internal_waters'
    TERRITORIAL_SEA = 'territorial_sea'
    CONTIGUOUS_AREA = 'contiguous_area'
    EXCLUSIVE_ECONOMIC_ZONE = 'exclusive_economic_zone'
    CONTINENTAL_SHELF = 'continental_shelf'
    VOID_UNK = 'void_unk'


class FormOfWayValue(DomainEnum):
    MOTORWAY = 'motorway'
    FREEWAY = 'freeway'
    SLIP_ROAD = 'slip_road'
    SERVICE_ROAD = 'service_road'
    DUAL_CARRIAGE_WAY = 'dual_carriage_way'
    SINGLE_CARRIAGE_WAY = 'single_carriage_way'
    ENCLOSED_TRAFFIC_AREA = 'enclosed_traffic_area'
    TRAFFIC_SQUARE = 'traffic_square'
    ROUNDABOUT = 'roundabout',
    ENTRANCE_OR_EXIT_CAR_PARK = 'entrance_or_exit_car_park'
    ENTRANCE_OR_EXIT_SERVICE = 'entrance_or_exit_service'
    PEDESTRIAN_zONE = 'pedestrian_zone'
    WALKWAY = 'walkway'
    TRACTOR_ROAD = 'tractor_road'
    BICYCLE_ROAD = 'bicycle_road'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class TENTNetworkValue(DomainEnum):
    CORE_TENT_NETWORK = 'core_tent_network'
    COMPREHENSIVE_TENT_NETWORK = 'comprehensive_tent_network'
    NO_TENT_NETWORK = 'no_tent_network'
    VOID_WILDCARD = 'void_*'


class ConditionOfFacilityValue(DomainEnum):
    DISUSED = 'disused'
    DECOMMISSIONED = 'decommissioned'
    FUNCTIONAL = 'functional'
    UNDER_CONSTRUCTION = 'under_construction'
    PROJECTED = 'projected'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class FunctionalRoadClass(DomainEnum):
    MAIN_ROAD = 'main-road'
    FIRST_CLASS = 'first_class'
    SECOND_CLASS = 'second_class'
    THIRD_CLASS = 'third_class'
    FOURTH_CLASS = 'fourth_class'
    FIFTH_CLASS = 'fifth_class'
    SIXTH_CLASS = 'sixth_class'
    SEVENTH_CLASS = 'seventh_class'
    EIGHTH_CLASS = 'eighth_class'
    NINTH_CLASS = 'ninth_class'


class TrafficFlowDirectionValue(DomainEnum):
    BOTH_DIRECTIONS = 'both_directions'
    INDIRECTION = 'indirection'
    OPPOSITE_DIRECTION = 'opposite_direction'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class VerticalPositionValue(DomainEnum):
    ON_GROUND_LEVEL = 'on_ground_level'
    SUSPENDED_OR_ELEVATED = 'suspended_or_elevated'
    UNDERGROUND = 'underground'
    VOID_UNK = 'void_unk'


class RoadSurfaceCategoryValue(DomainEnum):
    PAVED = 'paved'
    UNPAVED = 'unpaved'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class AccessRestrictionValue(DomainEnum):
    FORBIDDEN_LEGALLY = 'forbidden_legally'
    PHYSICALLY_IMPOSSIBLE = 'physically_impossible'
    PRIVATE = 'private'
    PUBLIC_ACCESS = 'public_access'
    SEASONAL = 'seasonal'
    TOLL = 'toll'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class FormOfRoadNodeValue(DomainEnum):
    ENCLOSED_TRAFFIC_AREA = 'enclosed_traffic_area'
    INTERCHANGE = 'interchange'
    JUNCTION = 'junction'
    LEVEL_CROSSING = 'level_crossing'
    PSEUDO_NODE = 'pseudo_node'
    ROAD_END = 'road_end'
    TRAFFIC_SQUARE = 'traffic_square'
    ROAD_SERVICE_AREA = 'road_service_area'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class RoadServiceTypeValue(DomainEnum):
    BUS_STATION = 'bus_station'
    PARKING = 'parking'
    REST_AREA = 'rest_area'
    ELECTRIC_CAR_LOADING_STATION = 'electric_car_loading_station'
    TOLL = 'toll'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class RailwayTypeValue(DomainEnum):
    COG_RAILWAY = 'cog_railway'
    FUNICULAR = 'funicular'
    MAGNETIC_LEVITATION = 'magnetic_levitation'
    METRO = 'metro'
    MONORAIL = 'monorail'
    TRAIN = 'train'
    TRAMWAY = 'tramway'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class ElectrifiedValue(DomainEnum):
    TRUE = 'true'
    FALSE = 'false'
    VOID_UNK = 'void_unk'


class RailwayStationUseValue(DomainEnum):
    CAR_SHUTTLE = 'car_shuttle'
    CARGO = 'cargo'
    MIXED = 'mixed'
    PASSENGERS = 'passengers'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class AerodromeCategoryValue(DomainEnum):
    INTERNATIONAL = 'international'
    DOMESTIC_NATIONAL = 'domestic_national'
    DOMESTIC_REGIONAL = 'domestic_regional'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class AerodromeTypeValue(DomainEnum):
    AERODROME_HELIPORT = 'aerodrome_heliport'
    AERODROME_ONLY = 'aerodrome_only'
    HELIPORT_ONLY = 'heliport_only'
    LANDING_SITE = 'landing_site'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class UseRestrictionValue(DomainEnum):
    RESERVED_FOR_MILITARY = 'reserved_for_military'
    TEMPORAL_RESTRICTIONS = 'temporal_restrictions'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class SurfaceCategoryValue(DomainEnum):
    ASPHALT = 'asphalt'
    CONCRETE = 'concrete'
    GRASS = 'grass'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class FerryUseValue(DomainEnum):
    CARS = 'cars'
    PASSENGERS = 'passengers'
    TRAIN = 'train'
    TRUCKS = 'trucks'
    VOID_UNK = 'void_unk'
    VOID_WILDCARD = 'void_*'


class CountryCodeValue(DomainEnum):
    ALBANIA = 'al'
    AUSTRIA = 'at'
    BELGIUM = 'be'
    BOSNIA_AND_HERZEGOVINA = 'ba'
    BULGARIA = 'bg'
    CROATIA = 'hr'
    CYPRUS = 'cy'
    CZECH_REPUBLIC = 'cz'
    DENMARK = 'dk'
    GREENLAND = 'gl'
    FAROE_ISLANDS = 'fo'
    ESTONIA = 'ee'
    FINLAND = 'fi'
    FRANCE = 'fr'
    MONACO = 'mc'
    GUADELOUPE = 'gp'
    FRENCH_GUIANA = 'gf'
    MARTINIQUE = 'mq'
    REUNION = 're'
    MAYOTTE = 'yt'
    SAINT_MARTIN = 'mf'
    SAINT_BARTHELEMY = 'bl'
    SAINT_PIERRE_AND_MIQUELON = 'pm'
    GERMANY = 'de'
    GREECE = 'gr'
    HUNGARY = 'hu'
    ICELAND = 'is'
    IRELAND = 'ie'
    ITALY = 'it'
    SAN_MARINO = 'sm'
    VATICAN_CITY_STATE = 'va'
    KOSOVO = 'ks'
    LATVIA = 'lv'
    LITHUANIA = 'lt'
    LUXEMBOURG = 'lu'
    REPUBLIC_OF_NORTH_MACEDONIA = 'mk'
    MALTA = 'mt'
    REPUBLIC_OF_MOLDOVA = 'md'
    NETHERLANDS = 'nl'
    NORWAY = 'no'
    SVALBARD_AND_JAN_MAYEN = 'sj'
    POLAND = 'pl'
    PORTUGAL = 'pt'
    ROMANIA = 'ro'
    SERBIA = 'rs'
    SLOVAKIA = 'sk'
    SLOVENIA = 'si'
    SPAIN = 'es'
    ANDORRA = 'ad'
    GIBRALTAR = 'gi'
    SWEDEN = 'se'
    SWITZERLAND = 'ch'
    LIECHTENSTEIN = 'li'
    GREAT_BRITAIN = 'gb'
    NORTHERN_IRELAND = 'nd'
    UKRAINE = 'ua'
