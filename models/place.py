#!/usr/bin/python3
"""place module. Contains class Place
Inherits from BaseModel class
"""
from models.base_model import BaseModel


class Place(BaseModel):
    """Place class

    Attributes:
        city_id (public, class attribute): string, default empty -> ""
                                            will be the City.id
        user_id (public, class attribute): string, default empty -> ""
                                            will be the User.id
        name (public, class attribute): string, default empty -> ""
        description (public, class attribute): string, default empty -> ""
        number_rooms (public, class attribute): integer, default 0
        number_bathrooms (public, class attribute): integer, default 0
        max_guest (public, class attribute): integer, default 0
        price_by_night (public, class attribute): integer, default 0
        latitude (public, class attribute): float, default 0.0
        longitude (public, class attribute): float, default 0.0
        amenity_ids (public, class attribute): list of string,
                                            default empty list.
                                            will be list of Amenity.id
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
