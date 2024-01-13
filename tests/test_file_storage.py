#!/usr/bin/python3
"""Unittest for FileStorage class
file name: test_file_storage.py
"""
import unittest
import inspect  # test function and module doc string
import pep8  # test pep8 conformance
# from json import dumps, loads #to test the de/serialization
from models.engine.file_storage import FileStorage
import models.engine.file_storage as file_storage
from models import storage


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
        result = style.check_files(['tests/test_file_storage.py'])
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

    def test_file_path(self):
        """Test file path"""
        self.assertTrue(hasattr(FileStorage, "_FileStorage__file_path"))
        self.assertEqual(self.__file_path,
                         "file.json")

    def test_all(self):
        """Test all"""
        self.assertTrue(hasattr(FileStorage, "all"))
        self.assertEqual(type(storage.all()), dict)
        self.assertIs(storage.all(),
                      storage._FileStorage__objects)

    # def tearDown(self) -> None:

# class TestFileStorageClassBreaking(unittest.TestCase):
#     """unittest class for BaseModel class when everything breaks"""
#     pass
