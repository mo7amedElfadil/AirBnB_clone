#!/usr/bin/python3
"""Unittest for base_model class
file name: test_base_model.py
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
import pycodestyle as pep8
from models.base_model import BaseModel
import models.base_model as base_model
from models import storage


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_base(self) -> None:
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self) -> None:
        """Test that the test_base_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = base_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(BaseModel.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(BaseModel, inspect.ismethod))
        for func in base_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestBaseModelClassWorking(unittest.TestCase):
    """unittest class for BaseModel class when everything works"""
    def setUp(self) -> None:
        """Set up instances and variables"""
        self.__file_path = storage._FileStorage__file_path
        self.instances = [BaseModel()]
        self.instances.append(BaseModel())
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.iso_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.fake_base = {"id": 0, "created_at": datetime.now().isoformat(),
                          "updated_at": datetime.now().isoformat(),
                          "first_name": "Mohamed"}

    def test_create_save(self) -> None:
        """Test default object creation and verify if
        storage.save is called when saving a new instance
        """
        with patch('models.storage.save') as save_mock:
            new = BaseModel()
            self.instances.append(new)
            new.save()
            save_mock.assert_called()

    def test_attributes(self) -> None:
        """test the attributes of the instance of BaseModel
        """
        base = self.instances[0]
        self.assertIsInstance(base, BaseModel)
        self.assertTrue(hasattr(base, "id"))
        self.assertTrue(hasattr(base, "created_at"))
        self.assertTrue(hasattr(base, "updated_at"))
        # test attributes type
        self.assertIsInstance(base.id, str)
        self.assertIsInstance(base.created_at, datetime)
        self.assertIsInstance(base.updated_at, datetime)
        # TODO: determine if test is necessary as values are same
        # self.assertNotEqual(base.created_at, base.updated_at)
        # test methods
        self.assertTrue(hasattr(base, "__init__"))
        self.assertTrue(hasattr(base, "__str__"))
        self.assertTrue(hasattr(base, "save"))
        self.assertTrue(hasattr(base, "to_dict"))

    def test_id(self) -> None:
        """test the id attribute of the instance of BaseModel
        """
        base = self.instances[0]
        new = self.instances[1]
        # test id not equal
        self.assertNotEqual(base.id, new.id)
        # test id type
        self.assertIsInstance(base.id, str)
        # test id is uuid4 format
        self.assertRegex(base.id, self.id_pattern)

    def test_str(self) -> None:
        """test the string represenation of the instance of BaseModel
        """
        base = self.instances[0]
        new = self.instances[1]
        # test instance str representation
        self.assertIsInstance(str(base), str)
        # test each instance unique
        self.assertNotEqual(str(base), str(new))
        # test str matches regex
        self.assertRegex(str(base), self.str_pattern)
        match = self.str_pattern.match(str(base))
        # test correct values represented
        self.assertEqual(match.group(1), base.__class__.__name__)
        self.assertEqual(match.group(2), base.id)
        self.assertEqual(match.group(3), str(base.__dict__))
        # test same class instance has same value
        self.assertEqual(match.group(1), new.__class__.__name__)
        with redirect_stdout(StringIO()) as f:
            print(base)
        self.assertEqual(f.getvalue().strip(), str(base))

    def test_to_dict(self) -> None:
        """test the to_dict method of the instance of BaseModel
        """
        base = self.instances[0]
        dic = base.__dict__
        to_dic = base.to_dict()
        for k, v in dic.items():
            if k not in ["created_at", "updated_at"]:
                self.assertEqual(v, to_dic[k])
        self.assertEqual(type(base).__name__, to_dic["__class__"])
        self.assertEqual(base.created_at.isoformat(), to_dic["created_at"])
        self.assertEqual(base.updated_at.isoformat(), to_dic["updated_at"])
        self.assertEqual(base.created_at,
                         datetime.fromisoformat(to_dic["created_at"]))
        self.assertEqual(base.updated_at,
                         datetime.fromisoformat(to_dic["updated_at"]))

    def test_init_kwarg_creation(self) -> None:
        """test creation of an instance of BaseModel using kwargs
        """
        base = self.instances[0]
        kw_base = BaseModel(**base.to_dict())
        self.assertEqual(base.id, kw_base.id)
        self.assertEqual(base.to_dict(), kw_base.to_dict())

    def test_init_kwarg_creation_not_exist(self) -> None:

        """test creation of an instance of BaseModel using kwargs
        """
        kw_base = BaseModel(**self.fake_base)
        self.assertEqual(self.fake_base["id"], kw_base.id)
        self.assertEqual(self.fake_base["created_at"],
                         kw_base.created_at.isoformat())
        self.assertEqual(self.fake_base["updated_at"],
                         kw_base.updated_at.isoformat())
        self.assertEqual(self.fake_base["first_name"],
                         kw_base.first_name)

    def test_update_attributes(self) -> None:
        """test updating the attributes of the instance of BaseModel
        """
        base = self.instances[0]
        # test updating
        base.first_name = "Mohamed"
        key = base.__class__.__name__ + "." + base.id

        self.assertEqual(base.first_name, "Mohamed")
        self.assertEqual(base.to_dict()["first_name"], "Mohamed")
        self.assertTrue(storage.all()[key] is base)
        self.assertTrue(hasattr(storage.all()[key], "first_name"))

        setattr(base, "last_name", "Elfadil")
        self.assertTrue(hasattr(base, "last_name"))
        self.assertTrue(hasattr(storage.all()[key], "last_name"))

        # test deleting
        del base.first_name
        self.assertFalse(hasattr(base, "first_name"))

    def test_datetime(self) -> None:
        """test the datetime attributes of the instance of BaseModel
        """
        base = self.instances[0]
        # test datetime
        self.assertIsInstance(base.created_at, datetime)
        try:
            datetime.strptime(base.to_dict()["created_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

        self.assertIsInstance(base.updated_at, datetime)
        try:
            datetime.strptime(base.to_dict()["updated_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

    def test_saving(self) -> None:
        """test the FileStorage saving of the instance of BaseModel
        """
        base = self.instances[0]
        key = base.__class__.__name__ + "." + base.id
        # test saving
        old_updated = base.updated_at
        sleep(0.00000001)
        base.save()
        # test updated at changed
        self.assertNotEqual(old_updated, base.updated_at)
        self.assertLess(old_updated, base.updated_at)
        # test stored
        self.assertTrue(base in storage.all().values())
        self.assertTrue(hasattr(storage.all()[base.__class__.__name__ +
                                              "." + base.id], "updated_at"))
        try:
            self.assertTrue(os.path.exists(self.__file_path))
            with open(self.__file_path, "r", encoding="utf-8") as f:
                content = load(f)
        except IOError:
            pass
        self.assertIn(key, content)
        self.assertEqual(content[key], base.to_dict())

    def test_deleting(self) -> None:
        """test the FileStorage deleting of the instance of BaseModel
        """
        # test deleting
        new2 = BaseModel()
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
            del storage.all()[f"{instance.__class__.__name__}.{instance.id}"]
        storage.save()
