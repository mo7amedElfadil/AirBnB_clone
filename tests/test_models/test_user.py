#!/usr/bin/python3
"""Unittest for user_model class
file name: test_user_model.py
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
from models.user import User
from models.base_model import BaseModel
import models.user as user_model
from models import storage


class TestUserDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_user(self) -> None:
        """Test that the user_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_user(self) -> None:
        """Test that the test_user_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_user_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = user_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(User.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        user_funcs = inspect.getmembers(User, inspect.isfunction)
        user_funcs.extend(inspect.getmembers(User, inspect.ismethod))
        for func in user_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestUserClassWorking(unittest.TestCase):
    """unittest class for User class when everything works"""
    def setUp(self) -> None:
        """Set up instances and variables"""
        self.__file_path = storage._FileStorage__file_path
        self.instances = [User()]
        self.instances.append(User())
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.iso_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.fake_user = {"id": 0, "created_at": datetime.now().isoformat(),
                          "updated_at": datetime.now().isoformat(),
                          "email": "my_email@gmail.com",
                          "password": "my_password",
                          "last_name": "Elfadil",
                          "first_name": "Mohamed"}

    def test_create_save(self) -> None:
        """Test default object creation and verify if
        storage.save is called when saving a new instance
        """
        with patch('models.storage.save') as save_mock:
            new = User()
            self.instances.append(new)
            new.save()
            save_mock.assert_called()

    def test_attributes(self) -> None:
        """test the attributes of the instance of User
        """
        user = self.instances[0]

        self.assertIsInstance(user, User)
        self.assertIsInstance(user, BaseModel)
        self.assertTrue(hasattr(user, "id"))
        self.assertTrue(hasattr(user, "created_at"))
        self.assertTrue(hasattr(user, "updated_at"))
        self.assertTrue(hasattr(user, "email"))
        self.assertTrue(hasattr(user, "password"))
        self.assertTrue(hasattr(user, "first_name"))
        self.assertTrue(hasattr(user, "last_name"))
        # test attributes type
        self.assertIsInstance(user.id, str)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)
        self.assertIsInstance(user.email, str)
        self.assertIsInstance(user.password, str)
        self.assertIsInstance(user.first_name, str)
        self.assertIsInstance(user.last_name, str)
        # TODO: determine if test is necessary as values are same
        # self.assertNotEqual(user.created_at, user.updated_at)
        # test methods
        self.assertTrue(hasattr(user, "__init__"))
        self.assertTrue(hasattr(user, "__str__"))
        self.assertTrue(hasattr(user, "save"))
        self.assertTrue(hasattr(user, "to_dict"))

    def test_id(self) -> None:
        """test the id attribute of the instance of User
        """
        user = self.instances[0]
        new = self.instances[1]
        # test id not equal
        self.assertNotEqual(user.id, new.id)
        # test id type
        self.assertIsInstance(user.id, str)
        # test id is uuid4 format
        self.assertRegex(user.id, self.id_pattern)

    def test_str(self) -> None:
        """test the string represenation of the instance of User
        """
        user = self.instances[0]
        new = self.instances[1]
        # test instance str representation
        self.assertIsInstance(str(user), str)
        # test each instance unique
        self.assertNotEqual(str(user), str(new))
        # test str matches regex
        self.assertRegex(str(user), self.str_pattern)
        match = self.str_pattern.match(str(user))
        # test correct values represented
        self.assertEqual(match.group(1), user.__class__.__name__)
        self.assertEqual(match.group(2), user.id)
        self.assertEqual(match.group(3), str(user.__dict__))
        # test same class instance has same value
        self.assertEqual(match.group(1), new.__class__.__name__)
        with redirect_stdout(StringIO()) as f:
            print(user)
        self.assertEqual(f.getvalue().strip(), str(user))

    def test_to_dict(self) -> None:
        """test the to_dict method of the instance of User
        """
        user = self.instances[0]
        dic = user.__dict__
        to_dic = user.to_dict()
        for k, v in dic.items():
            if k not in ["created_at", "updated_at"]:
                self.assertEqual(v, to_dic[k])
        self.assertEqual(type(user).__name__, to_dic["__class__"])
        self.assertEqual(user.created_at.isoformat(), to_dic["created_at"])
        self.assertEqual(user.updated_at.isoformat(), to_dic["updated_at"])
        self.assertEqual(user.created_at,
                         datetime.fromisoformat(to_dic["created_at"]))
        self.assertEqual(user.updated_at,
                         datetime.fromisoformat(to_dic["updated_at"]))

    def test_init_kwarg_creation(self) -> None:
        """test creation of an instance of User using kwargs
        """
        user = self.instances[0]
        kw_user = User(**user.to_dict())
        self.assertEqual(user.id, kw_user.id)
        self.assertEqual(user.to_dict(), kw_user.to_dict())

    def test_init_kwarg_creation_not_exist(self) -> None:
        """test creation of an instance of User using kwargs
        """
        kw_user = User(**self.fake_user)
        self.assertEqual(self.fake_user["id"], kw_user.id)
        self.assertEqual(self.fake_user["created_at"],
                         kw_user.created_at.isoformat())
        self.assertEqual(self.fake_user["updated_at"],
                         kw_user.updated_at.isoformat())
        self.assertEqual(self.fake_user["first_name"],
                         kw_user.first_name)
        self.assertEqual(self.fake_user["last_name"],
                         kw_user.last_name)
        self.assertEqual(self.fake_user["email"],
                         kw_user.email)
        self.assertEqual(self.fake_user["password"],
                         kw_user.password)

    def test_update_attributes(self) -> None:
        """test updating the attributes of the instance of User
        """
        user = self.instances[0]
        # test updating
        user.string = "String"
        key = user.__class__.__name__ + "." + user.id

        self.assertEqual(user.string, "String")
        self.assertEqual(user.to_dict()["string"], "String")
        self.assertTrue(storage.all()[key] is user)
        self.assertTrue(hasattr(storage.all()[key], "string"))

        setattr(user, "string2", "String2")
        self.assertTrue(hasattr(user, "string2"))
        self.assertTrue(hasattr(storage.all()[key], "string2"))
        # test deleting
        del user.string
        self.assertFalse(hasattr(user, "string"))

    def test_datetime(self) -> None:
        """test the datetime attributes of the instance of User
        """
        user = self.instances[0]
        # test datetime
        self.assertIsInstance(user.created_at, datetime)
        try:
            datetime.strptime(user.to_dict()["created_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

        self.assertIsInstance(user.updated_at, datetime)
        try:
            datetime.strptime(user.to_dict()["updated_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

    def test_saving(self) -> None:
        """test the FileStorage saving of the instance of User
        """
        user = self.instances[0]

        key = user.__class__.__name__ + "." + user.id
        # test saving
        old_updated = user.updated_at
        sleep(0.00000001)
        user.save()
        # test updated at changed
        self.assertNotEqual(old_updated, user.updated_at)
        self.assertLess(old_updated, user.updated_at)
        # test stored
        self.assertTrue(user in storage.all().values())
        self.assertTrue(hasattr(storage.all()[user.__class__.__name__ +
                                              "." + user.id], "updated_at"))
        try:
            self.assertTrue(os.path.exists(self.__file_path))
            with open(self.__file_path, "r", encoding="utf-8") as f:
                content = load(f)
        except IOError:
            pass
        self.assertIn(key, content)
        self.assertEqual(content[key], user.to_dict())

    def test_deleting(self) -> None:
        """test the FileStorage deleting of the instance of User
        """
        # test deleting
        new2 = User()
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
