#!/usr/bin/python3
"""review module. Contains class Review
Inherits from BaseModel class
"""
from models.base_model import BaseModel

class Review(BaseModel):
    """Review class

    Attributes:
        place_id (public, class attribute): string, default empty -> ""
                                            will be Place.id
        user_id (public, class attribute): string, default empty -> ""
                                            will be User.id
        text (public, class attribute): string, default empty -> ""
    """
    place_id = ""
    user_id = ""
    text = ""
