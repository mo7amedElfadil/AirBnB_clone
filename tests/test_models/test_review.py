#!/usr/bin/python3
"""Unittest for review_model class
file name: test_review_model.py
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
from models.review import Review
from models.base_model import BaseModel
import models.review as review_model
from models import storage


class TestReviewDocPep8(unittest.TestCase):
    """unittest class for Base class documentation and pep8 conformaty"""
    def test_pep8_review(self) -> None:
        """Test that the review_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_review(self) -> None:
        """Test that the test_review_module conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self) -> None:
        """test module documentation"""
        mod_doc = review_model.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self) -> None:
        """test class documentation"""
        mod_doc = str(Review.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self) -> None:
        """Tests for the presence of docstrings in all functions"""
        review_funcs = inspect.getmembers(Review, inspect.isfunction)
        review_funcs.extend(inspect.getmembers(Review, inspect.ismethod))
        for func in review_funcs:
            self.assertIsNotNone(func[1].__doc__)
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestReviewClassWorking(unittest.TestCase):
    """unittest class for Review class when everything works"""
    def setUp(self) -> None:
        """Set up instances and variables"""
        self.__file_path = storage._FileStorage__file_path
        self.instances = [Review()]
        self.instances.append(Review())
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.iso_format = '%Y-%m-%dT%H:%M:%S.%f'
        self.fake_review = {"id": 0, "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat(),
                            "place_id": "86d024c5-b956-4639-be75-59ac2bff0983",
                            "user_id": "56d024c5-b956-4639-be75-59ac2bff0983",
                            "text": "This is a fake review"}

    def test_create_save(self) -> None:
        """Test default object creation and verify if
        storage.save is called when saving a new instance
        """
        with patch('models.storage.save') as save_mock:
            new = Review()
            self.instances.append(new)
            new.save()
            save_mock.assert_called()

    def test_attributes(self) -> None:
        """test the attributes of the instance of Review
        """
        review = self.instances[0]

        self.assertIsInstance(review, Review)
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))
        self.assertTrue(hasattr(review, "place_id"))
        self.assertTrue(hasattr(review, "user_id"))
        self.assertTrue(hasattr(review, "text"))
        # test attributes type
        self.assertIsInstance(review.id, str)
        self.assertIsInstance(review.created_at, datetime)
        self.assertIsInstance(review.updated_at, datetime)
        self.assertIsInstance(review.place_id, str)
        self.assertIsInstance(review.user_id, str)
        self.assertIsInstance(review.text, str)
        # TODO: determine if test is necessary as values are same
        # self.assertNotEqual(review.created_at, review.updated_at)
        # test methods
        self.assertTrue(hasattr(review, "__init__"))
        self.assertTrue(hasattr(review, "__str__"))
        self.assertTrue(hasattr(review, "save"))
        self.assertTrue(hasattr(review, "to_dict"))

    def test_id(self) -> None:
        """test the id attribute of the instance of Review
        """
        review = self.instances[0]
        new = self.instances[1]
        # test id not equal
        self.assertNotEqual(review.id, new.id)
        # test id type
        self.assertIsInstance(review.id, str)
        # test id is uuid4 format
        self.assertRegex(review.id, self.id_pattern)

    def test_str(self) -> None:
        """test the string represenation of the instance of Review
        """
        review = self.instances[0]
        new = self.instances[1]
        # test instance str representation
        self.assertIsInstance(str(review), str)
        # test each instance unique
        self.assertNotEqual(str(review), str(new))
        # test str matches regex
        self.assertRegex(str(review), self.str_pattern)
        match = self.str_pattern.match(str(review))
        # test correct values represented
        self.assertEqual(match.group(1), review.__class__.__name__)
        self.assertEqual(match.group(2), review.id)
        self.assertEqual(match.group(3), str(review.__dict__))
        # test same class instance has same value
        self.assertEqual(match.group(1), new.__class__.__name__)
        with redirect_stdout(StringIO()) as f:
            print(review)
        self.assertEqual(f.getvalue().strip(), str(review))

    def test_to_dict(self) -> None:
        """test the to_dict method of the instance of Review
        """
        review = self.instances[0]
        dic = review.__dict__
        to_dic = review.to_dict()
        for k, v in dic.items():
            if k not in ["created_at", "updated_at"]:
                self.assertEqual(v, to_dic[k])
        self.assertEqual(type(review).__name__, to_dic["__class__"])
        self.assertEqual(review.created_at.isoformat(), to_dic["created_at"])
        self.assertEqual(review.updated_at.isoformat(), to_dic["updated_at"])
        self.assertEqual(review.created_at,
                         datetime.fromisoformat(to_dic["created_at"]))
        self.assertEqual(review.updated_at,
                         datetime.fromisoformat(to_dic["updated_at"]))

    def test_init_kwarg_creation(self) -> None:
        """test creation of an instance of Review using kwargs
        """
        review = self.instances[0]
        kw_review = Review(**review.to_dict())
        self.assertEqual(review.id, kw_review.id)
        self.assertEqual(review.to_dict(), kw_review.to_dict())

    def test_init_kwarg_creation_not_exist(self) -> None:
        """test creation of an instance of Review using kwargs
        """
        kw_review = Review(**self.fake_review)
        self.assertEqual(self.fake_review["id"], kw_review.id)
        self.assertEqual(self.fake_review["created_at"],
                         kw_review.created_at.isoformat())
        self.assertEqual(self.fake_review["updated_at"],
                         kw_review.updated_at.isoformat())
        self.assertEqual(self.fake_review["place_id"],
                         kw_review.place_id)
        self.assertEqual(self.fake_review["user_id"],
                         kw_review.user_id)
        self.assertEqual(self.fake_review["text"],
                         kw_review.text)

    def test_update_attributes(self) -> None:
        """test updating the attributes of the instance of Review
        """
        review = self.instances[0]
        # test updating
        review.string = "String"
        key = review.__class__.__name__ + "." + review.id

        self.assertEqual(review.string, "String")
        self.assertEqual(review.to_dict()["string"], "String")
        self.assertTrue(storage.all()[key] is review)
        self.assertTrue(hasattr(storage.all()[key], "string"))

        setattr(review, "string2", "String2")
        self.assertTrue(hasattr(review, "string2"))
        self.assertTrue(hasattr(storage.all()[key], "string2"))
        # test deleting
        del review.string
        self.assertFalse(hasattr(review, "string"))

    def test_datetime(self) -> None:
        """test the datetime attributes of the instance of Review
        """
        review = self.instances[0]
        # test datetime
        self.assertIsInstance(review.created_at, datetime)
        try:
            datetime.strptime(review.to_dict()["created_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

        self.assertIsInstance(review.updated_at, datetime)
        try:
            datetime.strptime(review.to_dict()["updated_at"],
                              self.iso_format)
        except ValueError:
            self.fail()

    def test_saving(self) -> None:
        """test the FileStorage saving of the instance of Review
        """
        review = self.instances[0]

        key = review.__class__.__name__ + "." + review.id
        # test saving
        old_updated = review.updated_at
        sleep(0.00000001)
        review.save()
        # test updated at changed
        self.assertNotEqual(old_updated, review.updated_at)
        self.assertLess(old_updated, review.updated_at)
        # test stored
        self.assertTrue(review in storage.all().values())
        self.assertTrue(hasattr(storage.all()[review.__class__.__name__ +
                                              "." + review.id], "updated_at"))
        try:
            self.assertTrue(os.path.exists(self.__file_path))
            with open(self.__file_path, "r", encoding="utf-8") as f:
                content = load(f)
        except IOError:
            pass
        self.assertIn(key, content)
        self.assertEqual(content[key], review.to_dict())

    def test_deleting(self) -> None:
        """test the FileStorage deleting of the instance of Review
        """
        # test deleting
        new2 = Review()
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
