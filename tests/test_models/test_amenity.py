#!/usr/bin/python3
"""Unittest for amenity_model class
file name: test_amenity_model.py
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
from models.amenity import Amenity
from models.base_model import BaseModel
import models.amenity as amenity_model
from models import storage


class TestAmenityDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_amenity(self) -> None:
        """Test that the amenity_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_amenity(self) -> None:
        """Test that the test_amenity_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_models/test_amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = amenity_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(Amenity.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        amenity_funcs = inspect.getmembers(Amenity, inspect.isfunction)
        amenity_funcs.extend(inspect.getmembers(Amenity, inspect.ismethod))
        for func in amenity_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestAmenityClassWorking(unittest.TestCase):
    """unittest class for Amenity class when everything works"""
    def setUp(self) -> None:
        """Set up instances and variables"""
        self.__file_path = storage._FileStorage__file_path
        self.instances = [Amenity()]
        self.instances.append(Amenity())
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.iso_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.fake_amenity = {"id": 0, "created_at": datetime.now().isoformat(),
                             "updated_at": datetime.now().isoformat(),
                             "name": "Kitchen"}

    def test_create_save(self) -> None:
        """Test default object creation and verify if
        storage.save is called when saving a new instance
        """
        with patch('models.storage.save') as save_mock:
            new = Amenity()
            self.instances.append(new)
            new.save()
            save_mock.assert_called()

    def test_attributes(self) -> None:
        """test the attributes of the instance of Amenity
        """
        amenity = self.instances[0]

        self.assertIsInstance(amenity, Amenity)
        self.assertIsInstance(amenity, BaseModel)
        self.assertTrue(hasattr(amenity, "id"))
        self.assertTrue(hasattr(amenity, "created_at"))
        self.assertTrue(hasattr(amenity, "updated_at"))
        self.assertTrue(hasattr(amenity, "name"))
        # test attributes type
        self.assertIsInstance(amenity.id, str)
        self.assertIsInstance(amenity.created_at, datetime)
        self.assertIsInstance(amenity.updated_at, datetime)
        self.assertIsInstance(amenity.name, str)
        # TODO: determine if test is necessary as values are same
        # self.assertNotEqual(amenity.created_at, amenity.updated_at)
        # test methods
        self.assertTrue(hasattr(amenity, "__init__"))
        self.assertTrue(hasattr(amenity, "__str__"))
        self.assertTrue(hasattr(amenity, "save"))
        self.assertTrue(hasattr(amenity, "to_dict"))

    def test_id(self) -> None:
        """test the id attribute of the instance of Amenity
        """
        amenity = self.instances[0]
        new = self.instances[1]
        # test id not equal
        self.assertNotEqual(amenity.id, new.id)
        # test id type
        self.assertIsInstance(amenity.id, str)
        # test id is uuid4 format
        self.assertRegex(amenity.id, self.id_pattern)

    def test_str(self) -> None:
        """test the string represenation of the instance of Amenity
        """
        amenity = self.instances[0]
        new = self.instances[1]
        # test instance str representation
        self.assertIsInstance(str(amenity), str)
        # test each instance unique
        self.assertNotEqual(str(amenity), str(new))
        # test str matches regex
        self.assertRegex(str(amenity), self.str_pattern)
        match = self.str_pattern.match(str(amenity))
        # test correct values represented
        self.assertEqual(match.group(1), amenity.__class__.__name__)
        self.assertEqual(match.group(2), amenity.id)
        self.assertEqual(match.group(3), str(amenity.__dict__))
        # test same class instance has same value
        self.assertEqual(match.group(1), new.__class__.__name__)
        with redirect_stdout(StringIO()) as f:
            print(amenity)
        self.assertEqual(f.getvalue().strip(), str(amenity))

    def test_to_dict(self) -> None:
        """test the to_dict method of the instance of Amenity
        """
        amenity = self.instances[0]
        dic = amenity.__dict__
        to_dic = amenity.to_dict()
        for k, v in dic.items():
            if k not in ["created_at", "updated_at"]:
                self.assertEqual(v, to_dic[k])
        self.assertEqual(type(amenity).__name__, to_dic["__class__"])
        self.assertEqual(amenity.created_at.isoformat(), to_dic["created_at"])
        self.assertEqual(amenity.updated_at.isoformat(), to_dic["updated_at"])
        self.assertEqual(amenity.created_at,
                         datetime.fromisoformat(to_dic["created_at"]))
        self.assertEqual(amenity.updated_at,
                         datetime.fromisoformat(to_dic["updated_at"]))

    def test_init_kwarg_creation(self) -> None:
        """test creation of an instance of Amenity using kwargs
        """
        amenity = self.instances[0]
        kw_amenity = Amenity(**amenity.to_dict())
        self.assertEqual(amenity.id, kw_amenity.id)
        self.assertEqual(amenity.to_dict(), kw_amenity.to_dict())

    def test_init_kwarg_creation_not_exist(self) -> None:
        """test creation of an instance of Amenity using kwargs
        """
        kw_amenity = Amenity(**self.fake_amenity)
        self.assertEqual(self.fake_amenity["id"], kw_amenity.id)
        self.assertEqual(self.fake_amenity["created_at"],
                         kw_amenity.created_at.isoformat())
        self.assertEqual(self.fake_amenity["updated_at"],
                         kw_amenity.updated_at.isoformat())
        self.assertEqual(self.fake_amenity["name"],
                         kw_amenity.name)

    def test_update_attributes(self) -> None:
        """test updating the attributes of the instance of Amenity
        """
        amenity = self.instances[0]
        # test updating
        amenity.string = "String"
        key = amenity.__class__.__name__ + "." + amenity.id

        self.assertEqual(amenity.string, "String")
        self.assertEqual(amenity.to_dict()["string"], "String")
        self.assertTrue(storage.all()[key] is amenity)
        self.assertTrue(hasattr(storage.all()[key], "string"))

        setattr(amenity, "string2", "String2")
        self.assertTrue(hasattr(amenity, "string2"))
        self.assertTrue(hasattr(storage.all()[key], "string2"))
        # test deleting
        del amenity.string
        self.assertFalse(hasattr(amenity, "string"))

    def test_datetime(self) -> None:
        """test the datetime attributes of the instance of Amenity
        """
        amenity = self.instances[0]
        # test datetime
        self.assertIsInstance(amenity.created_at, datetime)
        try:
            datetime.strptime(amenity.to_dict()["created_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

        self.assertIsInstance(amenity.updated_at, datetime)
        try:
            datetime.strptime(amenity.to_dict()["updated_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

    def test_saving(self) -> None:
        """test the FileStorage saving of the instance of Amenity
        """
        amenity = self.instances[0]

        key = amenity.__class__.__name__ + "." + amenity.id
        # test saving
        old_updated = amenity.updated_at
        sleep(0.00000001)
        amenity.save()
        # test updated at changed
        self.assertNotEqual(old_updated, amenity.updated_at)
        self.assertLess(old_updated, amenity.updated_at)
        # test stored
        self.assertTrue(amenity in storage.all().values())
        self.assertTrue(hasattr(storage.all()[amenity.__class__.__name__ +
                                              "." + amenity.id], "updated_at"))
        try:
            self.assertTrue(os.path.exists(self.__file_path))
            with open(self.__file_path, "r", encoding="utf-8") as f:
                content = load(f)
        except IOError:
            pass
        self.assertIn(key, content)
        self.assertEqual(content[key], amenity.to_dict())

    def test_deleting(self) -> None:
        """test the FileStorage deleting of the instance of Amenity
        """
        # test deleting
        new2 = Amenity()
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
