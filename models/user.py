#!/usr/bin/python3
"""user module. Contains class User
Inherits from BaseModel class
"""
from models.base_model import BaseModel

<<<<<<< HEAD
=======

>>>>>>> main
class User(BaseModel):
    """User class

    Attributes:
        email (public, class attribute): string, default empty -> ""
        password (public, class attribute): string, default empty -> ""
        first_name (public, class attribute): string, default empty -> ""
        last_name (public, class attribute): string, default empty -> ""
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
