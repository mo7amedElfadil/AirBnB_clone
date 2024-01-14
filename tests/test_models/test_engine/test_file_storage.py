#!/usr/bin/python3
"""Unittest for FileStorage class
file name: test_file_storage.py
"""
import os
import unittest
from unittest.mock import patch
from json import load
import inspect  # test function and module doc string
# import pep8  # test pep8 conformance
import pycodestyle as pep8
from models.engine.file_storage import FileStorage
import models.engine.file_storage as file_storage
from models import storage
from models.base_model import BaseModel
from console import HBNBCommand


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for FileStorage class
    documentation and pep8 conformaty"""
    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_file_storage conforms to PEP8."""
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_models/test_engine/' +
                                    'test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation"""
        mod_doc = file_storage.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self):
        """test class documentation"""
        mod_doc = str(FileStorage.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions"""
        base_funcs = inspect.getmembers(FileStorage, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(FileStorage, inspect.ismethod))
        for func in base_funcs:
            self.assertTrue(len(str(func[1].__doc__)) > 0)


# TODO: Test cases for FS
class TestFileStorageClassWorking(unittest.TestCase):
    """unittest class for FileStorage class when everything works"""
    def setUp(self) -> None:
        """Set up instances and variables"""
        self.__file_path = storage._FileStorage__file_path
        self.instances = [BaseModel()]
        storage.save()

    def test_attributes(self):
        """Test file path"""
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertEqual(self.__file_path,
                         "file.json")
        self.assertTrue(hasattr(FileStorage, "_FileStorage__objects"))
        self.assertTrue(hasattr(FileStorage, "all"))
        self.assertTrue(hasattr(FileStorage, "new"))
        self.assertTrue(hasattr(FileStorage, "save"))
        self.assertTrue(hasattr(FileStorage, "reload"))

    def test_all(self):
        """Test all"""
        self.assertEqual(type(storage.all()), dict)
        self.instances.append(BaseModel())
        storage.save()
        self.assertTrue(self.instances[0] in storage.all().values())
        key = f"BaseModel.{self.instances[0].id}"
        self.assertTrue(os.path.exists(self.__file_path))
        with open(self.__file_path, 'r', encoding='utf-8') as f:
            self.assertIn(key, load(f))

        self.assertIs(storage.all(),
                      storage._FileStorage__objects)
        self.assertIn("BaseModel.{}".format(self.instances[0].id),
                      storage.all().keys())
        self.assertIs(storage.all()[f"BaseModel.{self.instances[0].id}"],
                      self.instances[0])

    def test_new(self):
        """Test new"""
        with patch('models.storage.new') as new_mock:
            new = BaseModel()
            new.save()
            new_mock.assert_called()
        self.instances.append(BaseModel())
        storage.save()
        key = f"BaseModel.{self.instances[1].id}"
        self.assertIn(key, storage.all())
        self.assertIs(storage.all()[key], self.instances[1])

    def test_save(self):
        """Test save"""
        with patch('models.storage.save') as save_mock:
            new = BaseModel()
            self.instances.append(new)
            new.save()
            save_mock.assert_called()
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            f.write('')
        with open(self.__file_path, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), '')
        storage.save()
        with open(self.__file_path, 'r', encoding='utf-8') as f:
            self.assertNotEqual(f.read(), '')

    def test_reload(self):
        """Test reload"""
        with patch('models.storage.reload') as reload_mock:
            storage.reload()
            reload_mock.assert_called()
        storage.all().clear()
        self.assertEqual(storage.all(), {})
        storage.reload()
        self.assertNotEqual(storage.all(), {})
        with open(self.__file_path, 'r', encoding='utf-8') as f:
            content = load(f)
        for key, value in storage.all().items():
            self.assertTrue(key in content)
            self.assertEqual(value.to_dict(), content[key])

    def tearDown(self) -> None:
        """Tear down instances and variables"""
        for instance in self.instances:
            del storage.all()[instance.__class__.__name__ +
                              "." + instance.id]
        storage.save()
