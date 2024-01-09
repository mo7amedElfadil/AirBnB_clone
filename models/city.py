#!/usr/bin/python3
"""city module. Contains class City
Inherits from BaseModel class
"""
from models.base_model import BaseModel

class City(BaseModel):
    """City class

    Attributes:
        state_id (public, class attribute): string, default empty -> ""
                                            will be the State.id
        name (public, class attribute): string, default empty -> ""
    """
    state_id = ""
    name = ""
