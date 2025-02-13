import enum


class Operation(enum.Enum):
    RENT = "rent"
    SALE = "sale"


class PropertyType(enum.Enum):
    HOMES = "homes"
    NEW_DEVELOPMENTS = "newDevelopments"
    BEDROOMS = "bedrooms"
    OFFICES = "offices"
    PREMISES = "premises"
    TRANSFERS = "transfers"
    GARAGES = "garages"
    LANDS = "lands"
    STORAGE_ROOMS = "storageRooms"
    BUILDINGS = "buildings"


class Typology(enum.Enum):
    HOUSES_OR_CHALETS = "housesOrChalets"
    FLATS = "flats"


class SubTypology(enum.Enum):
    INDEPENDANT_HOUSE = "independantHouse"
    SEMIDETACHED_HOUSE = "semidetachedHouse"
    TERRACED_HOUSE = "terracedHouse"
    APARTMENT = "apartmentoType"


class RentalUsage(enum.Enum):
    LONG_TERM = "longTerm"
    SEASONAL = "seasonal"


class Gender(enum.Enum):
    MA = 'male'
    FE = 'female'


class TenantOccupation(enum.Enum):
    STUDENTS = 'students'
    WORKERS = 'workers'


class FloorHeights(enum.Enum):
    TOP = 'topFloor'
    INTERMEDIATE = 'intermediateFloor'
    GROUND = 'groundFloor'


class BedType(enum.Enum):
    SINGLE = 'single'
    DOUBLE = 'double'
    TWO_BEDS = 'twoBeds'
    NO_BED = 'none'


class Preservation(enum.Enum):
    NEW_DEVELOPMENT = 'newDevelopment'
    GOOD_CONDITION = 'good'
    NEEDS_REFORM = 'renew'
