import json
from typing import Optional, Set, Literal

from api import COUNTRY
from model import Operation, PropertyType, Gender, BedType, FloorHeights, TenantOccupation, RentalUsage, Preservation, \
    SubTypology, Geometry
from utils import to_comma_separated_string


class SearchFilterBuilder:
    def __init__(self):
        self.filters = {
            "operation": Operation.RENT.value,
            "propertyType": PropertyType.HOMES.value,
            "maxItems": 100,
            "numPage": 1,
            "showRuledOuts": True,

            "locale": COUNTRY,
            "quality": "high",
            "gallery": True,
        }
        self.operation_set = False  # Controlador para asegurarse de que se aplica un solo conjunto de filtros

    # Métodos para los parámetros generales
    def set_operation(self, operation: Operation):
        self.filters["operation"] = operation.value
        self.operation_set = True
        return self

    def set_property_type(self, property_type: PropertyType):
        self.filters["propertyType"] = property_type.value
        return self

    def set_max_items(self, max_items: int):
        self.filters["maxItems"] = max_items
        return self

    def set_price_range(self, min_price: int = 0, max_price: int = 0):
        if min_price:
            self.filters["minPrice"] = min_price
        if max_price:
            self.filters["maxPrice"] = max_price
        return self

    def set_size_range(self, min_size: int = 0, max_size: int = 0):
        if min_size:
            self.filters["minSize"] = min_size
        if max_size:
            self.filters["maxSize"] = max_size
        return self

    def set_bedrooms(self, bedrooms: Optional[Set[Literal[0, 1, 2, 3, 4]]]):
        if bedrooms:
            self.filters["bedrooms"] = ",".join(str(b) for b in bedrooms)
        return self

    def set_bathrooms(self, bathrooms: Optional[Set[Literal[1, 2, 3]]]):
        if bathrooms:
            self.filters["bathrooms"] = ",".join(str(b) for b in bathrooms)
        return self

    def set_num_page(self, num_page: int) -> 'SearchFilterBuilder':
        self.filters["numPage"] = num_page
        return self

    def set_since_date(self, since_date: Optional[Literal['T', 'W', 'M']]):
        if since_date:
            self.filters["sinceDate"] = since_date
        return self

    def set_location_id(self, location_id: str):
        if location_id:
            self.filters["locationId"] = location_id
        return self

    def set_location_name(self, location_name: str):
        if location_name:
            self.filters["locationName"] = location_name
        return self

    def set_show_ruled_outs(self, show_ruled_outs: bool):
        self.filters["showRuledOuts"] = show_ruled_outs
        return self

    def set_shape(self, shape: Geometry):
        if shape:
            self.filters["shape"] = json.dumps(shape.to_dict())
        return self

    def set_shape_from_json(self, shape: str):
        if shape:
            self.filters["shape"] = json.dumps(shape)
        return self

    def set_room_filters(self, *, gender: Gender,
                         smoking_allowed: Optional[bool] = None,
                         pets_allowed: Optional[bool] = None,
                         bed_type: Optional[BedType] = None,
                         available_from: Optional[str] = None,
                         online_booking: Optional[bool] = None,
                         housemates: Optional[Set[Literal[2, 3, 4]]] = None,
                         # meaning 2, 3, >=4, respectively (including you as the first housemate)
                         couples_allowed: Optional[bool] = None,
                         children_allowed: Optional[bool] = None,
                         street_view_window: Optional[bool] = None,
                         private_toilet: Optional[bool] = None,
                         air_conditioning: Optional[bool] = None,
                         elevator: Optional[bool] = None,
                         terrace: Optional[bool] = None,
                         exterior: Optional[bool] = None,
                         accessible: Optional[bool] = None,
                         housekeeper_included: Optional[bool] = None,
                         garden: Optional[bool] = None,
                         swimming_pool: Optional[bool] = None,
                         floor_heights: Optional[Set[FloorHeights]] = None,
                         tenant_occupation: Optional[Set[TenantOccupation]] = None,
                         lgbt_friendly: Optional[bool] = None,
                         owner_not_living: Optional[bool] = None,
                         private_owner: Optional[bool] = None):

        if gender is None:
            raise ValueError("You must specify a gender.")

        if self.operation_set != Operation.RENT or self.filters["propertyType"] != PropertyType.BEDROOMS.value:
            raise ValueError("Operation (RENT) and property type (BEDROOMS) must be set before applying filters.")

        self.filters.update({
            "newGender": gender,
            "smokingPolicy": (
                "allowed" if smoking_allowed else "disallowed") if smoking_allowed is not None else None,
            "petsPolicy": ("allowed" if pets_allowed else "disallowed") if pets_allowed is not None else None,
            "bedType": bed_type,
            "availableFrom": available_from,
            "onlineBooking": online_booking,
            "housemates": to_comma_separated_string(housemates),
            "couplesAllowed": couples_allowed,
            "childrenAllowed": children_allowed,
            "streetViewWindow": street_view_window,
            "privateToilet": private_toilet,
            "airConditioning": air_conditioning,
            "elevator": elevator,
            "terrace": terrace,
            "exterior": exterior,
            "accessible": accessible,
            "hasHouseKeeper": housekeeper_included,
            "garden": garden,
            "swimmingPool": swimming_pool,
            "floorHeights": to_comma_separated_string(floor_heights),
            "occupation": to_comma_separated_string(tenant_occupation),
            "gayPartners": lgbt_friendly,
            "ownerNotLiving": owner_not_living,
            "privateOwner": private_owner,
        })
        return self

    def set_home_filters(self, *,
                         rental_usages: Optional[Set[RentalUsage]] = None,
                         is_flat: Optional[bool] = None,
                         is_penthouse: Optional[bool] = None,
                         is_duplex: Optional[bool] = None,
                         is_independant: Optional[bool] = None,
                         is_semi_detached: Optional[bool] = None,
                         is_terraced: Optional[bool] = None,
                         is_apartment: Optional[bool] = None,
                         is_country_house: Optional[bool] = None,
                         balcony: Optional[bool] = None,
                         terrace: Optional[bool] = None,
                         exterior: Optional[bool] = None,
                         preservations: Optional[Set[Preservation]] = None,
                         furnished: Optional[bool] = None,
                         pets_allowed: Optional[bool] = None,
                         air_conditioning: Optional[bool] = None,
                         builtin_wardrobes: Optional[bool] = None,
                         elevator: Optional[bool] = None,
                         garage: Optional[bool] = None,
                         garden: Optional[bool] = None,
                         swimming_pool: Optional[bool] = None,
                         store_room: Optional[bool] = None,
                         accessible: Optional[bool] = None,
                         luxury: Optional[bool] = None,
                         floor_heights: Optional[Set[FloorHeights]] = None,
                         has_plan: Optional[bool] = None,
                         virtual_tour: Optional[bool] = None,
                         bank_offer: Optional[bool] = None
                         ):
        if self.operation_set != Operation.RENT or self.filters["propertyType"] != PropertyType.HOMES.value:
            raise ValueError("Operation (RENT) and property type (HOMES) must be set before applying filters.")

        # Handle specific home types
        _flat = None
        if is_flat and is_penthouse and is_duplex:
            is_flat = None
            is_penthouse = None
            is_duplex = None
            _flat = True

        # Validate and add sub-typology
        sub_typology_set: Optional[Set[SubTypology]] = set()
        if is_independant:
            sub_typology_set.add(SubTypology.INDEPENDANT_HOUSE)
        if is_semi_detached:
            sub_typology_set.add(SubTypology.SEMIDETACHED_HOUSE)
        if is_terraced:
            sub_typology_set.add(SubTypology.TERRACED_HOUSE)
        if is_apartment:
            sub_typology_set.add(SubTypology.APARTMENT)

        # Handle combinations of typologies (if rustic)
        _chalet = None
        if SubTypology.INDEPENDANT_HOUSE in sub_typology_set and SubTypology.SEMIDETACHED_HOUSE in sub_typology_set and SubTypology.TERRACED_HOUSE in sub_typology_set and is_country_house:
            sub_typology_set = {x for x in sub_typology_set if x not in (
                SubTypology.INDEPENDANT_HOUSE, SubTypology.SEMIDETACHED_HOUSE, SubTypology.TERRACED_HOUSE)}
            is_country_house = None
            _chalet = True

        if len(sub_typology_set) == 0:
            sub_typology_set = None

        _exterior_domestic_space = False
        if balcony and terrace:
            balcony = None
            terrace = None
            _exterior_domestic_space = True

        # Update home filters
        self.filters.update({
            "rentalUsages": to_comma_separated_string(rental_usages),
            "onlyFlats": is_flat,
            "penthouse": is_penthouse,
            "duplex": is_duplex,
            "flat": _flat,
            "countryHouse": is_country_house,
            "chalet": _chalet,
            "subTypology": to_comma_separated_string(sub_typology_set),
            "preservations": to_comma_separated_string(preservations),
            "furnished": furnished,
            "petsAllowed": pets_allowed,
            "airConditioning": air_conditioning,
            "builtinWardrobes": builtin_wardrobes,
            "elevator": elevator,
            "balcony": balcony,
            "terrance": terrace,  # yeah, 'terraNce' is a typo in the API; BUT it's a typo in the API, so we have to keep it
            "exteriorDomesticSpace": _exterior_domestic_space,
            "exterior": exterior,
            "garage": garage,
            "garden": garden,
            "swimmingPool": swimming_pool,
            "storeRoom": store_room,
            "accessible": accessible,
            "luxury": luxury,
            "floorHeights": to_comma_separated_string(floor_heights),
            "hasPlan": has_plan,
            "virtualTour": virtual_tour,
            "bankOffer": bank_offer,
        })
        return self

    def build(self):
        if not self.operation_set:
            raise ValueError("Operation must be set before building the search filter.")

        return {k: v for k, v in self.filters.items() if v is not None}
