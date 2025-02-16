import enum
from typing import Tuple
from abc import ABC, abstractmethod
from typing import List


class Operation(enum.Enum):
    RENT = "rent"
    SALE = "sale"
    SHARE = "share"
    TRANSFERS = "transfers"


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


class Position:
    def __init__(self, lon: float, lat: float, elevation: float = 0):
        self.lon = lon
        self.lat = lat
        self.elevation = elevation

    def __repr__(self):
        return f"Position({self.lon}, {self.lat}, {self.elevation})"

    def to_tuple(self) -> Tuple[float, float, float]:
        return self.lon, self.lat, self.elevation

    @staticmethod
    def from_dict(coord: Tuple[float, float, float]) -> 'Position':
        return Position(coord[0], coord[1], coord[2] if len(coord) > 2 else 0)


class Ring:
    def __init__(self, positions: List[Position]):
        if positions[0] != positions[-1]:
            positions.append(positions[0])  # Cerrar el anillo
        self.positions = positions

    def __repr__(self):
        return f"Ring({self.positions})"

    @staticmethod
    def from_dict(coords: List[Tuple[float, float, float]]) -> 'Ring':
        positions = [Position.from_dict(coord) for coord in coords]
        return Ring(positions)


class Geometry(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def __repr__(self):
        pass


class Polygon(Geometry):
    def __init__(self, ring: Ring):
        self.ring = ring

    def to_dict(self) -> dict:
        return {
            "type": "Polygon",
            "coordinates": [[pos.to_tuple() for pos in self.ring.positions]]
        }

    def __repr__(self):
        return f"Polygon({self.ring})"

    @staticmethod
    def from_dict(data: dict) -> 'Polygon':
        # Asegurarse que el JSON esté bien formado y que 'coordinates' sea una lista
        coords = data.get("coordinates", [])
        if not coords:
            raise ValueError("El JSON no contiene coordenadas válidas para un Polygon")
        return Polygon(Ring.from_dict(coords[0]))


class MultiPolygon(Geometry):
    def __init__(self, polygons: List[Polygon]):
        self.polygons = polygons

    def to_dict(self) -> dict:
        return {
            "type": "MultiPolygon",
            "coordinates": [
                [[pos.to_tuple() for pos in polygon.ring.positions] for polygon in self.polygons]
            ]
        }

    def __repr__(self):
        return f"MultiPolygon({self.polygons})"

    @staticmethod
    def from_dict(data: dict) -> 'MultiPolygon':
        polygons = []
        for coords in data.get("coordinates", []):
            polygons.append(Polygon.from_dict({"coordinates": coords}))
        return MultiPolygon(polygons)
