#!/usr/bin/python3
"""Unittest for state_model class
file name: test_state_model.py
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
from models.state import State
from models.base_model import BaseModel
import models.state as state_model
from models import storage


class TestStateDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_state(self) -> None:
        """Test that the state_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_state(self) -> None:
        """Test that the test_state_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_state_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = state_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(State.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        state_funcs = inspect.getmembers(State, inspect.isfunction)
        state_funcs.extend(inspect.getmembers(State, inspect.ismethod))
        for func in state_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestStateClassWorking(unittest.TestCase):
    """unittest class for State class when everything works"""
    def setUp(self) -> None:
        """Set up instances and variables"""
        self.__file_path = storage._FileStorage__file_path
        self.instances = [State()]
        self.instances.append(State())
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.iso_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.fake_state = {"id": 0, "created_at": datetime.now().isoformat(),
                           "updated_at": datetime.now().isoformat(),
                           "name": "Wyoming"}

    def test_create_save(self) -> None:
        """Test default object creation and verify if
        storage.save is called when saving a new instance
        """
        with patch('models.storage.save') as save_mock:
            new = State()
            self.instances.append(new)
            new.save()
            save_mock.assert_called()

    def test_attributes(self) -> None:
        """test the attributes of the instance of State
        """
        state = self.instances[0]

        self.assertIsInstance(state, State)
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))
        self.assertTrue(hasattr(state, "name"))
        # test attributes type
        self.assertIsInstance(state.id, str)
        self.assertIsInstance(state.created_at, datetime)
        self.assertIsInstance(state.updated_at, datetime)
        self.assertIsInstance(state.name, str)
        # TODO: determine if test is necessary as values are same
        # self.assertNotEqual(state.created_at, state.updated_at)
        # test methods
        self.assertTrue(hasattr(state, "__init__"))
        self.assertTrue(hasattr(state, "__str__"))
        self.assertTrue(hasattr(state, "save"))
        self.assertTrue(hasattr(state, "to_dict"))

    def test_id(self) -> None:
        """test the id attribute of the instance of State
        """
        state = self.instances[0]
        new = self.instances[1]
        # test id not equal
        self.assertNotEqual(state.id, new.id)
        # test id type
        self.assertIsInstance(state.id, str)
        # test id is uuid4 format
        self.assertRegex(state.id, self.id_pattern)

    def test_str(self) -> None:
        """test the string represenation of the instance of State
        """
        state = self.instances[0]
        new = self.instances[1]
        # test instance str representation
        self.assertIsInstance(str(state), str)
        # test each instance unique
        self.assertNotEqual(str(state), str(new))
        # test str matches regex
        self.assertRegex(str(state), self.str_pattern)
        match = self.str_pattern.match(str(state))
        # test correct values represented
        self.assertEqual(match.group(1), state.__class__.__name__)
        self.assertEqual(match.group(2), state.id)
        self.assertEqual(match.group(3), str(state.__dict__))
        # test same class instance has same value
        self.assertEqual(match.group(1), new.__class__.__name__)
        with redirect_stdout(StringIO()) as f:
            print(state)
        self.assertEqual(f.getvalue().strip(), str(state))

    def test_to_dict(self) -> None:
        """test the to_dict method of the instance of State
        """
        state = self.instances[0]
        dic = state.__dict__
        to_dic = state.to_dict()
        for k, v in dic.items():
            if k not in ["created_at", "updated_at"]:
                self.assertEqual(v, to_dic[k])
        self.assertEqual(type(state).__name__, to_dic["__class__"])
        self.assertEqual(state.created_at.isoformat(), to_dic["created_at"])
        self.assertEqual(state.updated_at.isoformat(), to_dic["updated_at"])
        self.assertEqual(state.created_at,
                         datetime.fromisoformat(to_dic["created_at"]))
        self.assertEqual(state.updated_at,
                         datetime.fromisoformat(to_dic["updated_at"]))

    def test_init_kwarg_creation(self) -> None:
        """test creation of an instance of State using kwargs
        """
        state = self.instances[0]
        kw_state = State(**state.to_dict())
        self.assertEqual(state.id, kw_state.id)
        self.assertEqual(state.to_dict(), kw_state.to_dict())

    def test_init_kwarg_creation_not_exist(self) -> None:
        """test creation of an instance of State using kwargs
        """
        kw_state = State(**self.fake_state)
        self.assertEqual(self.fake_state["id"], kw_state.id)
        self.assertEqual(self.fake_state["created_at"],
                         kw_state.created_at.isoformat())
        self.assertEqual(self.fake_state["updated_at"],
                         kw_state.updated_at.isoformat())
        self.assertEqual(self.fake_state["name"],
                         kw_state.name)

    def test_update_attributes(self) -> None:
        """test updating the attributes of the instance of State
        """
        state = self.instances[0]
        # test updating
        state.string = "String"
        key = state.__class__.__name__ + "." + state.id

        self.assertEqual(state.string, "String")
        self.assertEqual(state.to_dict()["string"], "String")
        self.assertTrue(storage.all()[key] is state)
        self.assertTrue(hasattr(storage.all()[key], "string"))

        setattr(state, "string2", "String2")
        self.assertTrue(hasattr(state, "string2"))
        self.assertTrue(hasattr(storage.all()[key], "string2"))
        # test deleting
        del state.string
        self.assertFalse(hasattr(state, "string"))

    def test_datetime(self) -> None:
        """test the datetime attributes of the instance of State
        """
        state = self.instances[0]
        # test datetime
        self.assertIsInstance(state.created_at, datetime)
        try:
            datetime.strptime(state.to_dict()["created_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

        self.assertIsInstance(state.updated_at, datetime)
        try:
            datetime.strptime(state.to_dict()["updated_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

    def test_saving(self) -> None:
        """test the FileStorage saving of the instance of State
        """
        state = self.instances[0]

        key = state.__class__.__name__ + "." + state.id
        # test saving
        old_updated = state.updated_at
        sleep(0.00000001)
        state.save()
        # test updated at changed
        self.assertNotEqual(old_updated, state.updated_at)
        self.assertLess(old_updated, state.updated_at)
        # test stored
        self.assertTrue(state in storage.all().values())
        self.assertTrue(hasattr(storage.all()[state.__class__.__name__ +
                                              "." + state.id], "updated_at"))
        try:
            self.assertTrue(os.path.exists(self.__file_path))
            with open(self.__file_path, "r", encoding="utf-8") as f:
                content = load(f)
        except IOError:
            pass
        self.assertIn(key, content)
        self.assertEqual(content[key], state.to_dict())

    def test_deleting(self) -> None:
        """test the FileStorage deleting of the instance of State
        """
        # test deleting
        new2 = State()
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
