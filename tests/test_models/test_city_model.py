#!/usr/bin/python3
"""Unittest for city_model class
file name: test_city_model.py
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
from models.city import City
from models.base_model import BaseModel
import models.city as city_model
from models import storage


class TestCityDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_city(self) -> None:
        """Test that the city_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_city(self) -> None:
        """Test that the test_city_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_models/test_city_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = city_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(City.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        city_funcs = inspect.getmembers(City, inspect.isfunction)
        city_funcs.extend(inspect.getmembers(City, inspect.ismethod))
        for func in city_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestCityClassWorking(unittest.TestCase):
    """unittest class for City class when everything works"""
    def setUp(self) -> None:
        """Set up instances and variables"""
        self.__file_path = storage._FileStorage__file_path
        self.instances = [City()]
        self.instances.append(City())
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.iso_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.fake_city = {"id": 0, "created_at": datetime.now().isoformat(),
                          "updated_at": datetime.now().isoformat(),
                          "name": "Washington",
                          "state_id": "86d024c5-b956-4639-be75-59ac2bff0983"}

    def test_create_save(self) -> None:
        """Test default object creation and verify if
        storage.save is called when saving a new instance
        """
        with patch('models.storage.save') as save_mock:
            new = City()
            self.instances.append(new)
            new.save()
            save_mock.assert_called()

    def test_attributes(self) -> None:
        """test the attributes of the instance of City
        """
        city = self.instances[0]

        self.assertIsInstance(city, City)
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))
        self.assertTrue(hasattr(city, "name"))
        self.assertTrue(hasattr(city, "state_id"))
        # test attributes type
        self.assertIsInstance(city.id, str)
        self.assertIsInstance(city.created_at, datetime)
        self.assertIsInstance(city.updated_at, datetime)
        self.assertIsInstance(city.name, str)
        self.assertIsInstance(city.state_id, str)
        # TODO: determine if test is necessary as values are same
        # self.assertNotEqual(city.created_at, city.updated_at)
        # test methods
        self.assertTrue(hasattr(city, "__init__"))
        self.assertTrue(hasattr(city, "__str__"))
        self.assertTrue(hasattr(city, "save"))
        self.assertTrue(hasattr(city, "to_dict"))

    def test_id(self) -> None:
        """test the id attribute of the instance of City
        """
        city = self.instances[0]
        new = self.instances[1]
        # test id not equal
        self.assertNotEqual(city.id, new.id)
        # test id type
        self.assertIsInstance(city.id, str)
        # test id is uuid4 format
        self.assertRegex(city.id, self.id_pattern)

    def test_str(self) -> None:
        """test the string represenation of the instance of City
        """
        city = self.instances[0]
        new = self.instances[1]
        # test instance str representation
        self.assertIsInstance(str(city), str)
        # test each instance unique
        self.assertNotEqual(str(city), str(new))
        # test str matches regex
        self.assertRegex(str(city), self.str_pattern)
        match = self.str_pattern.match(str(city))
        # test correct values represented
        self.assertEqual(match.group(1), city.__class__.__name__)
        self.assertEqual(match.group(2), city.id)
        self.assertEqual(match.group(3), str(city.__dict__))
        # test same class instance has same value
        self.assertEqual(match.group(1), new.__class__.__name__)
        with redirect_stdout(StringIO()) as f:
            print(city)
        self.assertEqual(f.getvalue().strip(), str(city))

    def test_to_dict(self) -> None:
        """test the to_dict method of the instance of City
        """
        city = self.instances[0]
        dic = city.__dict__
        to_dic = city.to_dict()
        for k, v in dic.items():
            if k not in ["created_at", "updated_at"]:
                self.assertEqual(v, to_dic[k])
        self.assertEqual(type(city).__name__, to_dic["__class__"])
        self.assertEqual(city.created_at.isoformat(), to_dic["created_at"])
        self.assertEqual(city.updated_at.isoformat(), to_dic["updated_at"])
        self.assertEqual(city.created_at,
                         datetime.fromisoformat(to_dic["created_at"]))
        self.assertEqual(city.updated_at,
                         datetime.fromisoformat(to_dic["updated_at"]))

    def test_init_kwarg_creation(self) -> None:
        """test creation of an instance of City using kwargs
        """
        city = self.instances[0]
        kw_city = City(**city.to_dict())
        self.assertEqual(city.id, kw_city.id)
        self.assertEqual(city.to_dict(), kw_city.to_dict())

    def test_init_kwarg_creation_not_exist(self) -> None:
        """test creation of an instance of City using kwargs
        """
        kw_city = City(**self.fake_city)
        self.assertEqual(self.fake_city["id"], kw_city.id)
        self.assertEqual(self.fake_city["created_at"],
                         kw_city.created_at.isoformat())
        self.assertEqual(self.fake_city["updated_at"],
                         kw_city.updated_at.isoformat())
        self.assertEqual(self.fake_city["name"],
                         kw_city.name)
        self.assertEqual(self.fake_city["state_id"],
                         kw_city.state_id)

    def test_update_attributes(self) -> None:
        """test updating the attributes of the instance of City
        """
        city = self.instances[0]
        # test updating
        city.string = "String"
        key = city.__class__.__name__ + "." + city.id

        self.assertEqual(city.string, "String")
        self.assertEqual(city.to_dict()["string"], "String")
        self.assertTrue(storage.all()[key] is city)
        self.assertTrue(hasattr(storage.all()[key], "string"))

        setattr(city, "string2", "String2")
        self.assertTrue(hasattr(city, "string2"))
        self.assertTrue(hasattr(storage.all()[key], "string2"))
        # test deleting
        del city.string
        self.assertFalse(hasattr(city, "string"))

    def test_datetime(self) -> None:
        """test the datetime attributes of the instance of City
        """
        city = self.instances[0]
        # test datetime
        self.assertIsInstance(city.created_at, datetime)
        try:
            datetime.strptime(city.to_dict()["created_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

        self.assertIsInstance(city.updated_at, datetime)
        try:
            datetime.strptime(city.to_dict()["updated_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

    def test_saving(self) -> None:
        """test the FileStorage saving of the instance of City
        """
        city = self.instances[0]

        key = city.__class__.__name__ + "." + city.id
        # test saving
        old_updated = city.updated_at
        sleep(0.00000001)
        city.save()
        # test updated at changed
        self.assertNotEqual(old_updated, city.updated_at)
        self.assertLess(old_updated, city.updated_at)
        # test stored
        self.assertTrue(city in storage.all().values())
        self.assertTrue(hasattr(storage.all()[city.__class__.__name__ +
                                              "." + city.id], "updated_at"))
        try:
            self.assertTrue(os.path.exists(self.__file_path))
            with open(self.__file_path, "r", encoding="utf-8") as f:
                content = load(f)
        except IOError:
            pass
        self.assertIn(key, content)
        self.assertEqual(content[key], city.to_dict())

    def test_deleting(self) -> None:
        """test the FileStorage deleting of the instance of City
        """
        # test deleting
        new2 = City()
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
