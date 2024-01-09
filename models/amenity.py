#!/usr/bin/python3
"""amenity module. Contains class Amenity
Inherits from BaseModel class
"""
from models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity class

    Attributes:
        name (public, class attribute): string, default empty -> ""
    """
    name = ""
