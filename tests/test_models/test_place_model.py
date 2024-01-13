#!/usr/bin/python3
"""Unittest for place_model class
file name: test_place_model.py
"""
import os
from time import sleep
from datetime import datetime
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO
import inspect  # test function and module doc string
import re
from json import load  # , dump # to test the de/serialization
import pep8  # test pep8 conformance
from models.place import Place
from models.base_model import BaseModel
import models.place as place_model
from models import storage


class TestPlaceDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_place(self) -> None:
        """Test that the place_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_place(self) -> None:
        """Test that the test_place_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_models/test_place_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = place_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(Place.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        place_funcs = inspect.getmembers(Place, inspect.isfunction)
        place_funcs.extend(inspect.getmembers(Place, inspect.ismethod))
        for func in place_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestPlaceClassWorking(unittest.TestCase):
    """unittest class for Place class when everything works"""
    def setUp(self) -> None:
        """Set up instances and variables"""
        self.__file_path = storage._FileStorage__file_path
        self.instances = [Place()]
        self.instances.append(Place())
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.iso_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.fake_place = {"id": 0, "created_at": datetime.now().isoformat(),
                           "updated_at": datetime.now().isoformat(),
                           "city_id": "8td024c5-b956-4r39-bg75-5fdc2bff0983",
                           "user_id": "8td024c5-b956-4r39-bg75-5fdc2fsag9a3",
                           "name": "Holberton",
                           "description": "A place",
                           "number_rooms": 3,
                           "number_bathrooms": 2,
                           "max_guest": 3,
                           "price_by_night": 100,
                           "latitude": 1.1,
                           "longitude": 1.1,
                           "amenity_ids":
                           "86d024c5-b956-4639-be75-59ac2bff0983"}

    def test_create_save(self) -> None:
        """Test default object creation and verify if
        storage.save is called when saving a new instance
        """
        with patch('models.storage.save') as save_mock:
            new = Place()
            self.instances.append(new)
            new.save()
            save_mock.assert_called()

    def test_attributes(self) -> None:
        """test the attributes of the instance of Place
        """
        place = self.instances[0]

        self.assertIsInstance(place, Place)
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(hasattr(place, "id"))
        self.assertTrue(hasattr(place, "created_at"))
        self.assertTrue(hasattr(place, "updated_at"))
        self.assertTrue(hasattr(place, "city_id"))
        self.assertTrue(hasattr(place, "user_id"))
        self.assertTrue(hasattr(place, "name"))
        self.assertTrue(hasattr(place, "description"))
        self.assertTrue(hasattr(place, "number_rooms"))
        self.assertTrue(hasattr(place, "number_bathrooms"))
        self.assertTrue(hasattr(place, "max_guest"))
        self.assertTrue(hasattr(place, "price_by_night"))
        self.assertTrue(hasattr(place, "latitude"))
        self.assertTrue(hasattr(place, "longitude"))
        self.assertTrue(hasattr(place, "amenity_ids"))
        # test attributes type
        self.assertIsInstance(place.id, str)
        self.assertIsInstance(place.created_at, datetime)
        self.assertIsInstance(place.updated_at, datetime)
        self.assertIsInstance(place.city_id, str)
        self.assertIsInstance(place.user_id, str)
        self.assertIsInstance(place.name, str)
        self.assertIsInstance(place.description, str)
        self.assertIsInstance(place.number_rooms, int)
        self.assertIsInstance(place.number_bathrooms, int)
        self.assertIsInstance(place.max_guest, int)
        self.assertIsInstance(place.price_by_night, int)
        self.assertIsInstance(place.latitude, float)
        self.assertIsInstance(place.longitude, float)
        self.assertIsInstance(place.amenity_ids, list)

        # TODO: determine if test is necessary as values are same
        # self.assertNotEqual(place.created_at, place.updated_at)
        # test methods
        self.assertTrue(hasattr(place, "__init__"))
        self.assertTrue(hasattr(place, "__str__"))
        self.assertTrue(hasattr(place, "save"))
        self.assertTrue(hasattr(place, "to_dict"))

    def test_id(self) -> None:
        """test the id attribute of the instance of Place
        """
        place = self.instances[0]
        new = self.instances[1]
        # test id not equal
        self.assertNotEqual(place.id, new.id)
        # test id type
        self.assertIsInstance(place.id, str)
        # test id is uuid4 format
        self.assertRegex(place.id, self.id_pattern)

    def test_str(self) -> None:
        """test the string represenation of the instance of Place
        """
        place = self.instances[0]
        new = self.instances[1]
        # test instance str representation
        self.assertIsInstance(str(place), str)
        # test each instance unique
        self.assertNotEqual(str(place), str(new))
        # test str matches regex
        self.assertRegex(str(place), self.str_pattern)
        match = self.str_pattern.match(str(place))
        # test correct values represented
        self.assertEqual(match.group(1), place.__class__.__name__)
        self.assertEqual(match.group(2), place.id)
        self.assertEqual(match.group(3), str(place.__dict__))
        # test same class instance has same value
        self.assertEqual(match.group(1), new.__class__.__name__)
        with redirect_stdout(StringIO()) as f:
            print(place)
        self.assertEqual(f.getvalue().strip(), str(place))

    def test_to_dict(self) -> None:
        """test the to_dict method of the instance of Place
        """
        place = self.instances[0]
        dic = place.__dict__
        to_dic = place.to_dict()
        for k, v in dic.items():
            if k not in ["created_at", "updated_at"]:
                self.assertEqual(v, to_dic[k])
        self.assertEqual(type(place).__name__, to_dic["__class__"])
        self.assertEqual(place.created_at.isoformat(), to_dic["created_at"])
        self.assertEqual(place.updated_at.isoformat(), to_dic["updated_at"])
        self.assertEqual(place.created_at,
                         datetime.fromisoformat(to_dic["created_at"]))
        self.assertEqual(place.updated_at,
                         datetime.fromisoformat(to_dic["updated_at"]))

    def test_init_kwarg_creation(self) -> None:
        """test creation of an instance of Place using kwargs
        """
        place = self.instances[0]
        kw_place = Place(**place.to_dict())
        self.assertEqual(place.id, kw_place.id)
        self.assertEqual(place.to_dict(), kw_place.to_dict())

    def test_init_kwarg_creation_not_exist(self) -> None:
        """test creation of an instance of Place using kwargs
        """
        kw_place = Place(**self.fake_place)
        self.assertEqual(self.fake_place["id"], kw_place.id)
        self.assertEqual(self.fake_place["created_at"],
                         kw_place.created_at.isoformat())
        self.assertEqual(self.fake_place["updated_at"],
                         kw_place.updated_at.isoformat())
        self.assertEqual(self.fake_place["name"],
                         kw_place.name)
        self.assertEqual(self.fake_place["city_id"],
                         kw_place.city_id)
        self.assertEqual(self.fake_place["user_id"],
                         kw_place.user_id)
        self.assertEqual(self.fake_place["description"],
                         kw_place.description)
        self.assertEqual(self.fake_place["number_rooms"],
                         kw_place.number_rooms)
        self.assertEqual(self.fake_place["number_bathrooms"],
                         kw_place.number_bathrooms)
        self.assertEqual(self.fake_place["max_guest"],
                         kw_place.max_guest)
        self.assertEqual(self.fake_place["price_by_night"],
                         kw_place.price_by_night)
        self.assertEqual(self.fake_place["latitude"],
                         kw_place.latitude)
        self.assertEqual(self.fake_place["longitude"],
                         kw_place.longitude)
        self.assertEqual(self.fake_place["amenity_ids"],
                         kw_place.amenity_ids)

    def test_update_attributes(self) -> None:
        """test updating the attributes of the instance of Place
        """
        place = self.instances[0]
        # test updating
        place.string = "String"
        key = place.__class__.__name__ + "." + place.id

        self.assertEqual(place.string, "String")
        self.assertEqual(place.to_dict()["string"], "String")
        self.assertTrue(storage.all()[key] is place)
        self.assertTrue(hasattr(storage.all()[key], "string"))

        setattr(place, "string2", "String2")
        self.assertTrue(hasattr(place, "string2"))
        self.assertTrue(hasattr(storage.all()[key], "string2"))
        # test deleting
        del place.string
        self.assertFalse(hasattr(place, "string"))

    def test_datetime(self) -> None:
        """test the datetime attributes of the instance of Place
        """
        place = self.instances[0]
        # test datetime
        self.assertIsInstance(place.created_at, datetime)
        try:
            datetime.strptime(place.to_dict()["created_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

        self.assertIsInstance(place.updated_at, datetime)
        try:
            datetime.strptime(place.to_dict()["updated_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

    def test_saving(self) -> None:
        """test the FileStorage saving of the instance of Place
        """
        place = self.instances[0]

        key = place.__class__.__name__ + "." + place.id
        # test saving
        old_updated = place.updated_at
        sleep(0.00000001)
        place.save()
        # test updated at changed
        self.assertNotEqual(old_updated, place.updated_at)
        self.assertLess(old_updated, place.updated_at)
        # test stored
        self.assertTrue(place in storage.all().values())
        self.assertTrue(hasattr(storage.all()[place.__class__.__name__ +
                                              "." + place.id], "updated_at"))
        try:
            self.assertTrue(os.path.exists(self.__file_path))
            with open(self.__file_path, "r", encoding="utf-8") as f:
                content = load(f)
        except IOError:
            pass
        self.assertIn(key, content)
        self.assertEqual(content[key], place.to_dict())

    def test_deleting(self) -> None:
        """test the FileStorage deleting of the instance of Place
        """
        # test deleting
        new2 = Place()
        new2.save()
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                content = load(f).values()
        except IOError:
            pass
        self.assertTrue(new2.to_dict() in content)
        del storage.all()[new2.__class__.__name__ +
                          "." + new2.id]
        storage.save()
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                content = load(f).values()
        except IOError:
            pass
        self.assertFalse(new2.to_dict() in content)

    def tearDown(self) -> None:
        """Tear down instances and variables"""
        for instance in self.instances:
            del storage.all()[instance.__class__.__name__ +
                              "." + instance.id]
        storage.save()
