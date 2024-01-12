#!/usr/bin/python3
"""base_model module. Contains class BaseModel
All other classes will inherit from this class
"""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """BaseModel class

    Attributes:
        id (public, instance attribute): string uuid4
        created_at (public, instance attribute): datetime
        updated_at (public, instance attribute): datetime
    Methods:
        save: updates the public instance attribute updated_at
                with the current datetime
        to_dict: returns a dictionary containing all keys/values of
                __dict__ of the instance
    """
    def __init__(self, **kwargs) -> None:
        """Initialization of BaseModel Class"""
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            for k, v in kwargs.items():
                if k == "__class__":
                    continue
                if k in ["created_at", "updated_at"]:
                    setattr(self, k, datetime.fromisoformat(v))
                else:
                    setattr(self, k, v)

    def __str__(self) -> str:
        """returns the string representation of the class instance
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self) -> None:
        """updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self) -> dict:
        """returns a dictionary containing all keys/values of
        __dict__ of the instance
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = self.__class__.__name__
        if isinstance(my_dict["created_at"], datetime):
            my_dict["created_at"] = my_dict["created_at"].isoformat()
        if isinstance(my_dict["updated_at"], datetime):
            my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict
