#!/usr/bin/python3
"""file_storage module. Contains FileStorage class
file name: file_storage.py
"""
from json import dumps, loads
from json.decoder import JSONDecodeError


class FileStorage:
    """FileStorage class

    Attributes:

    Methods:
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
        self.__objects[obj.__class__.__name__ + "." + obj.id] = obj.to_dict()
        # print("objects:\n" ,self.__objects)

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)
        """
        try:
            print(self.__objects)
            with open(self.__file_path, "w", encoding="utf-8") as f:
                f.write(dumps(self.__objects))
        except IOError:
            pass
    def reload(self):
        """deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists ; otherwise, do nothing.
        If the file doesn’t exist, no exception should be raised)
        """
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                self.__objects = loads(f.read())
        except (IOError, JSONDecodeError):
            pass
