#!/usr/bin/python3
"""file_storage module. Contains FileStorage class
file name: file_storage.py
"""
from json import dump, load
from json.decoder import JSONDecodeError
from models.base_model import BaseModel


class FileStorage:
    """FileStorage class

    Attributes:
        __file_path (private, class attribute): string -
                            path to the JSON file (ex: file.json)
        __objects (private, class attribute): dictionary -
                            empty but will store all objects by
                            <class name>.id (ex: to store a BaseModel
                            object with id=12121212, the key will be
                            BaseModel.12121212)

    Methods:
        all(self): returns dictionary __objects
        new(self, obj): sets in __objects the obj with key <obj class name>.id
        save(self): serializes __objects to the JSON file (path: __file_path)
        reload(self): deserializes the JSON file to __objects
                    (only if the JSON file (__file_path) exists
                    otherwise no exception is raised)
    """
    __file_path = "file.json"
    __objects = {}


    def all(self) -> dict:
        """returns the dictionary __objects
        """
        return self.__objects

    def new(self, obj) -> None:
        """sets in __objects the obj with key <obj class name>.id
        """
        self.__objects[obj.__class__.__name__ + "." + obj.id] = obj

    def save(self) -> None:
        """serializes __objects to the JSON file (path: __file_path)
        """
        for k, v in self.__objects.items():
            self.__objects[k] = v.to_dict()
        try:
            with open(self.__file_path, "w", encoding="utf-8") as f:
                dump(self.__objects, f)
        except IOError:
            pass

    def reload(self) -> None:
        """deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists ; otherwise, do nothing.
        If the file doesn’t exist, no exception should be raised)
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for k, v in load(f).items():
                    self.__objects[k] = BaseModel(**v)
        except (IOError, JSONDecodeError):
            pass
