#!/usr/bin/python3
"""state module. Contains class State
Inherits from BaseModel class
"""
from models.base_model import BaseModel

class State(BaseModel):
    """State class

    Attributes:
        name (public, class attribute): string, default empty -> ""
    """
    name = ""
