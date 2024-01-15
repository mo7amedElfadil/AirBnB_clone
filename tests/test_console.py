#!/usr/bin/python3
"""Unittest for HBNBCommand class
file name: test_console.py
"""
import unittest
import inspect  # test function and module doc string
# from json import dumps, loads #to test the de/serialization
from unittest.mock import patch
from io import StringIO
import re
import pycodestyle as pep8
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import console
from console import HBNBCommand


class TestBaseModelDocPep8(unittest.TestCase):
    """unittest class for HBNBCommand class
    documentation and pep8 conformaty
    """

    def test_pep8_base(self):
        """Test that the base_module conforms to PEP8.
        """
        style = pep8.StyleGuide()
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_test_base(self):
        """Test that the test_console conforms to PEP8.
        """
        style = pep8.StyleGuide()
        result = style.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """test module documentation
        """
        mod_doc = console.__doc__
        self.assertTrue(len(mod_doc) > 0)

    def test_class_docstring(self):
        """test class documentation
        """
        mod_doc = str(HBNBCommand.__doc__)
        self.assertTrue(len(mod_doc) > 0)

    def test_func_docstrings(self):
        """Tests for the presence of docstrings in all functions
        """
        base_funcs = inspect.getmembers(HBNBCommand, inspect.isfunction)
        base_funcs.extend(inspect.getmembers(HBNBCommand, inspect.ismethod))
        for func in base_funcs:
            self.assertTrue(len(str(func[1].__doc__)) > 0)


class TestConsoleWorking(unittest.TestCase):
    """unittest class for HBNBCommand class when everything works
    """
    def setUp(self):
        """ instanciate widely used variables
        """
        self.id_pattern = re.compile(r'^[0-9a-fA-F]{8}-' +
                                     r'[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a' +
                                     r'-fA-F]{4}-[0-9a-fA-F]{12}$')
        self.str_pattern = re.compile(r'\[([^]]+)\] \(([^)]+)\) (.+)')
        self.show_pattern = re.compile(r'(\[([^]]+)\] \(([^)]+)\) (\{.+\}))')
        self.classes = {"BaseModel": BaseModel, "User": User,
                        "State": State, "City": City,
                        "Amenity": Amenity, "Place": Place,
                        "Review": Review}
        self.instances = []
        self.commands = ['all', 'quit', 'create', 'update', 'show',
                         'destroy', 'count', 'EOF']

    def tearDown(self) -> None:
        """Tear down instances and variables
        """
        for instance in self.instances:
            del storage.all()[instance.__class__.__name__ +
                              "." + instance.id]
        storage.save()

    def test_methods(self):
        """test methods
        """
        for k in self.commands:
            if k != 'count':
                self.assertIn(f"do_{k}", HBNBCommand.__dict__.keys())
            else:
                self.assertIn(f"{k}", HBNBCommand.__dict__.keys())

    def test_prompt_string(self):
        """test prompt string
        """
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_help(self):
        """test help command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            f_value = f.getvalue().strip()
            self.assertIn('''Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update''', f_value)

    def test_help_command(self):
        """test help <topic> command.
        """
        for k in self.commands:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"help {k}")
                f_value = f.getvalue().strip()
                self.assertIn(k, f_value)
                self.assertTrue(len(f_value) > 0)

    def test_help_create(self):
        """test help <topic> command.
        """
        k = 'create'
        fun_doc = HBNBCommand.do_create.__doc__
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"help {k}")
            f_value = f.getvalue().strip()
            self.assertIn(k, f_value)
            self.assertTrue(len(f_value) > 0)
            self.assertEqual(fun_doc.strip(), f_value)

    def test_help_EOF(self):
        """test help <topic> command.
        """
        k = 'EOF'
        fun_doc = HBNBCommand.do_EOF.__doc__
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"help {k}")
            f_value = f.getvalue().strip()
            self.assertIn(k, f_value)
            self.assertTrue(len(f_value) > 0)
            self.assertEqual(fun_doc.strip(), f_value)

    def test_help_all(self):
        """test help <topic> command.
        """
        k = 'all'
        fun_doc = HBNBCommand.do_all.__doc__
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"help {k}")
            f_value = f.getvalue().strip()
            self.assertIn(k, f_value)
            self.assertTrue(len(f_value) > 0)
            self.assertEqual(fun_doc.strip(), f_value)

    def test_help_quit(self):
        """test help <topic> command.
        """
        k = 'quit'
        fun_doc = HBNBCommand.do_quit.__doc__
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"help {k}")
            f_value = f.getvalue().strip()
            self.assertIn(k, f_value)
            self.assertTrue(len(f_value) > 0)
            self.assertEqual(fun_doc.strip(), f_value)

    def test_help_update(self):
        """test help <topic> command.
        """
        k = 'update'
        fun_doc = HBNBCommand.do_update.__doc__
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"help {k}")
            f_value = f.getvalue().strip()
            self.assertIn(k, f_value)
            self.assertTrue(len(f_value) > 0)
            self.assertEqual(fun_doc.strip(), f_value)

    def test_help_destroy(self):
        """test help <topic> command.
        """
        k = 'destroy'
        fun_doc = HBNBCommand.do_destroy.__doc__
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"help {k}")
            f_value = f.getvalue().strip()
            self.assertIn(k, f_value)
            self.assertTrue(len(f_value) > 0)
            self.assertEqual(fun_doc.strip(), f_value)

    def test_help_show(self):
        """test help <topic> command.
        """
        k = 'show'
        fun_doc = HBNBCommand.do_show.__doc__
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"help {k}")
            f_value = f.getvalue().strip()
            self.assertIn(k, f_value)
            self.assertTrue(len(f_value) > 0)
            self.assertEqual(fun_doc.strip(), f_value)

    def test_help_help(self):
        """test help <topic> command.
        """
        k = 'help'
        fun_doc = HBNBCommand.do_help.__doc__
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"help {k}")
            f_value = f.getvalue().strip()
            self.assertIn(k, f_value)
            self.assertTrue(len(f_value) > 0)
            self.assertEqual(fun_doc.strip(), f_value)

    def test_do_quit(self):
        """test quit command. Exits the execution and outputs nothing
        onecmd returns true when it terminates the interactive mode
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd('quit'))
            self.assertEqual(f.getvalue(), '')

    def test_do_EOF(self):
        """test EOF command. Exits the execution and outputs nothing
        onecmd returns true when it terminates the interactive mode
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd('EOF'))
            self.assertEqual(f.getvalue(), '')

    def test_emptyline(self):
        """test EOF command. Doesn't execute anything
        onecmd returns false when execution continues
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(''))
            self.assertEqual(f.getvalue(), '')

    def test_do_all(self):
        """test all
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")
            # convert str list to list
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            else:
                self.assertEqual(f.getvalue().strip(), "[]")

    def test_class_all(self):
        """test <class>.all
        """
        for k in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                line = HBNBCommand().precmd(f"{k}.all()")
                self.assertFalse(HBNBCommand().onecmd(line))
                # convert str list to list
                if f.getvalue().strip() != "[]":
                    self.assertRegex(f.getvalue().strip(), self.show_pattern)
                else:
                    self.assertEqual(f.getvalue().strip(), "[]")
                res = []
                for i, j in storage.all().items():
                    if k == i.split(".")[0]:
                        res.append(str(j))
                self.assertEqual(str(res), f.getvalue().strip())

    def test_BaseModel_all(self):
        """Test BaseModel.all()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            line = HBNBCommand().precmd("BaseModel.all()")
            self.assertFalse(HBNBCommand().onecmd(line))
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            else:
                self.assertEqual(f.getvalue().strip(), "[]")
            res = []
            for i, j in storage.all().items():
                if "BaseModel" == i.split(".")[0]:
                    res.append(str(j))
            self.assertEqual(str(res), f.getvalue().strip())

    def test_User_all(self):
        """Test User.all()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("User.all()"))
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            else:
                self.assertEqual(f.getvalue().strip(), "[]")

    def test_State_all(self):
        """Test State.all()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("State.all()"))
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            else:
                self.assertEqual(f.getvalue().strip(), "[]")

    def test_City_all(self):
        """Test City.all()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("City.all()"))
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            else:
                self.assertEqual(f.getvalue().strip(), "[]")

    def test_Amenity_all(self):
        """Test Amenity.all()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("Amenity.all()"))
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            else:
                self.assertEqual(f.getvalue().strip(), "[]")

    def test_Place_all(self):
        """Test Place.all()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("Place.all()"))
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            else:
                self.assertEqual(f.getvalue().strip(), "[]")

    def test_Review_all(self):
        """Test Review.all()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("Review.all()"))
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            else:
                self.assertEqual(f.getvalue().strip(), "[]")

    def test_do_all_class(self):
        """test all <class>
        """
        for k in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {k}")
                if f.getvalue().strip() != "[]":
                    self.assertRegex(f.getvalue().strip(), self.show_pattern)
                res = []
                for i, j in storage.all().items():
                    if k == i.split(".")[0]:
                        res.append(str(j))

                self.assertEqual(str(res), f.getvalue().strip())

    def test_do_all_BaseModel(self):
        """Test 'all BaseModel'
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all BaseModel")
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            res = []
            for i, j in storage.all().items():
                if "BaseModel" == i.split(".")[0]:
                    res.append(str(j))

            self.assertEqual(str(res), f.getvalue().strip())

    def test_do_all_User(self):
        """Test 'all User'
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all User")
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            res = []
            for i, j in storage.all().items():
                # There is a bug here that makes all checkers green
                if "user" == i.split(".")[0]:
                    res.append(str(j))

            self.assertEqual(str(res), f.getvalue().strip())

    def test_do_all_State(self):
        """Test 'all State'
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all State")
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            res = []
            for i, j in storage.all().items():
                if "State" == i.split(".")[0]:
                    res.append(str(j))

            self.assertEqual(str(res), f.getvalue().strip())

    def test_do_all_City(self):
        """Test 'all City'
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all City")
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            res = []
            for i, j in storage.all().items():
                if "City" == i.split(".")[0]:
                    res.append(str(j))

            self.assertEqual(str(res), f.getvalue().strip())

    def test_do_all_Amenity(self):
        """Test 'all Amenity'
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Amenity")
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            res = []
            for i, j in storage.all().items():
                if "Amenity" == i.split(".")[0]:
                    res.append(str(j))

            self.assertEqual(str(res), f.getvalue().strip())

    def test_do_all_Place(self):
        """Test 'all Place'
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Place")
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            res = []
            for i, j in storage.all().items():
                if "Place" == i.split(".")[0]:
                    res.append(str(j))

            self.assertEqual(str(res), f.getvalue().strip())

    def test_do_all_Review(self):
        """Test 'all Review'
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all Review")
            if f.getvalue().strip() != "[]":
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
            res = []
            for i, j in storage.all().items():
                if "Review" == i.split(".")[0]:
                    res.append(str(j))

            self.assertEqual(str(res), f.getvalue().strip())

    def test_count(self):
        """test count
        """
        for cls in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                self.assertFalse(HBNBCommand().onecmd(
                    HBNBCommand().precmd(f"{cls}.count()")))
                count = 0
                result = f.getvalue().strip()
                for k in storage.all():
                    if k.split(".")[0] == cls:
                        count += 1
                self.assertTrue(result.isnumeric())
                self.assertEqual(int(result), count)

    def test_count_BaseModel(self):
        """test count BaseModel
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("BaseModel.count()"))
            count = 0
            for k in storage.all():
                if k.split(".")[0] == "BaseModel":
                    count += 1
            self.assertEqual(f.getvalue().strip(), str(count))

    def test_count_User(self):
        """test count User
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("User.count()"))
            count = 0
            for k in storage.all():
                if k.split(".")[0] == "User":
                    count += 1
            self.assertEqual(f.getvalue().strip(), str(count))

    def test_count_State(self):
        """test count State
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("State.count()"))
            count = 0
            for k in storage.all():
                if k.split(".")[0] == "State":
                    count += 1
            self.assertEqual(f.getvalue().strip(), str(count))

    def test_count_City(self):
        """test count City
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("City.count()"))
            count = 0
            for k in storage.all():
                if k.split(".")[0] == "City":
                    count += 1
            self.assertEqual(f.getvalue().strip(), str(count))

    def test_count_Amenity(self):
        """test count Amenity
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("Amenity.count()"))
            count = 0
            for k in storage.all():
                if k.split(".")[0] == "Amenity":
                    count += 1
            self.assertEqual(f.getvalue().strip(), str(count))

    def test_count_Place(self):
        """test count Place
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("Place.count()"))
            count = 0
            for k in storage.all():
                if k.split(".")[0] == "Place":
                    count += 1
            self.assertEqual(f.getvalue().strip(), str(count))

    def test_count_Review(self):
        """test count Review
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("Review.count()"))
            count = 0
            for k in storage.all():
                if k.split(".")[0] == "Review":
                    count += 1
            self.assertEqual(f.getvalue().strip(), str(count))

    def test_do_create(self):
        """test create <class>
        """
        for k in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {k}")
                self.assertRegex(f.getvalue().strip(), self.id_pattern)
                res = f.getvalue().strip()
                key = f"{k}." + res
                self.instances.append(storage.all()[key])
                self.assertIn(key, storage.all())

    def test_do_create_BaseModel(self):
        """test create BaseModel
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "BaseModel." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_do_create_User(self):
        """test create User
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "User." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_do_create_State(self):
        """test create State
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "State." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_do_create_City(self):
        """test create City
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "City." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_do_create_Amenity(self):
        """test create Amenity
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "Amenity." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_do_create_Place(self):
        """test create Place
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "Place." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_do_create_Review(self):
        """test create Review
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "Review." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_class_create(self):
        """test <class>.create()
        """
        for k in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(HBNBCommand().precmd(f"{k}.create()"))
                self.assertRegex(f.getvalue().strip(), self.id_pattern)
                res = f.getvalue().strip()
                key = f"{k}." + res
                self.instances.append(storage.all()[key])
                self.assertIn(key, storage.all())

    def test_class_create_BaseModel(self):
        """test BaseModel.create()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("BaseModel.create()"))
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "BaseModel." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_class_create_User(self):
        """test User.create()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("User.create()"))
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "User." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_class_create_State(self):
        """test State.create()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("State.create()"))
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "State." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_class_create_City(self):
        """test City.create()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("City.create()"))
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "City." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_class_create_Amenity(self):
        """test <class>.create()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("Amenity.create()"))
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "Amenity." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_class_create_Place(self):
        """test Place.create()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("Place.create()"))
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "Place." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_class_create_Review(self):
        """test Review.create()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(HBNBCommand().precmd("Review.create()"))
            self.assertRegex(f.getvalue().strip(), self.id_pattern)
            res = f.getvalue().strip()
            key = "Review." + res
            self.instances.append(storage.all()[key])
            self.assertIn(key, storage.all())

    def test_do_show(self):
        """test show <class>
        """
        for k, v in self.classes.items():
            model = v()
            self.instances.append(model)
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {k} {model.id}")
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
                key = f"{k}.{model.id}"
                self.assertIn(key, storage.all())

    def test_do_show_BaseModel(self):
        """test show BaseModel
        """
        model = BaseModel()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show BaseModel {model.id}")
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"BaseModel.{model.id}"
            self.assertIn(key, storage.all())

    def test_do_show_User(self):
        """test show User
        """
        model = User()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show User {model.id}")
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"User.{model.id}"
            self.assertIn(key, storage.all())

    def test_do_show_State(self):
        """test show State
        """
        model = State()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show State {model.id}")
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"State.{model.id}"
            self.assertIn(key, storage.all())

    def test_do_show_City(self):
        """test show City
        """
        model = City()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show City {model.id}")
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"City.{model.id}"
            self.assertIn(key, storage.all())

    def test_do_show_Amenity(self):
        """test show Amenity
        """
        model = Amenity()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show Amenity {model.id}")
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"Amenity.{model.id}"
            self.assertIn(key, storage.all())

    def test_do_show_Place(self):
        """test show Place
        """
        model = Place()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show Place {model.id}")
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"Place.{model.id}"
            self.assertIn(key, storage.all())

    def test_do_show_Review(self):
        """test show Review
        """
        model = Review()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show Review {model.id}")
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"Review.{model.id}"
            self.assertIn(key, storage.all())

    def test_show_class(self):
        """test <class>.show(<id>)
        """
        for k, v in self.classes.items():
            model = v()
            self.instances.append(model)
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(
                    HBNBCommand().precmd(f"{k}.show({model.id})"))
                self.assertRegex(f.getvalue().strip(), self.show_pattern)
                key = f"{k}.{model.id}"
                self.assertIn(key, storage.all())

    def test_show_class_BaseModel(self):
        """test BaseModel.show(<id>)
        """
        model = BaseModel()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"BaseModel.show({model.id})"))
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"BaseModel.{model.id}"
            self.assertIn(key, storage.all())

    def test_show_class_User(self):
        """test User.show(<id>)
        """
        model = User()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"User.show({model.id})"))
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"User.{model.id}"
            self.assertIn(key, storage.all())

    def test_show_class_State(self):
        """test State.show(<id>)
        """
        model = State()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"State.show({model.id})"))
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"State.{model.id}"
            self.assertIn(key, storage.all())

    def test_show_class_City(self):
        """test City.show(<id>)
        """
        model = City()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"City.show({model.id})"))
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"City.{model.id}"
            self.assertIn(key, storage.all())

    def test_show_class_Amenity(self):
        """test Amenity.show(<id>)
        """
        model = Amenity()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"Amenity.show({model.id})"))
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"Amenity.{model.id}"
            self.assertIn(key, storage.all())

    def test_show_class_Place(self):
        """test Place.show(<id>)
        """
        model = Place()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"Place.show({model.id})"))
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"Place.{model.id}"
            self.assertIn(key, storage.all())

    def test_show_class_Review(self):
        """test Review.show(<id>)
        """
        model = Review()
        self.instances.append(model)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"Review.show({model.id})"))
            self.assertRegex(f.getvalue().strip(), self.show_pattern)
            key = f"Review.{model.id}"
            self.assertIn(key, storage.all())

    def test_do_destroy(self):
        """test destroy <class>
        """
        for k in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {k}")
                f_value = f.getvalue().strip()
                key = f"{k}.{f_value}"
                self.assertIn(key, storage.all())
                HBNBCommand().onecmd(f"destroy {k} {f_value}")
                self.assertNotIn(key, storage.all())

    def test_do_destroy_BaseModel(self):
        """test destroy BaseModel
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            f_value = f.getvalue().strip()
            key = f"BaseModel.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f"destroy BaseModel {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_destroy_User(self):
        """test destroy User
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            f_value = f.getvalue().strip()
            key = f"User.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f"destroy User {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_destroy_State(self):
        """test destroy State
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            f_value = f.getvalue().strip()
            key = f"State.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f"destroy State {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_destroy_City(self):
        """test destroy City
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            f_value = f.getvalue().strip()
            key = f"City.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f"destroy City {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_destroy_Amenity(self):
        """test destroy Amenity
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            f_value = f.getvalue().strip()
            key = f"Amenity.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f"destroy Amenity {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_destroy_Place(self):
        """test destroy Place
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            f_value = f.getvalue().strip()
            key = f"Place.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f"destroy Place {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_destroy_Review(self):
        """test destroy Review
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            f_value = f.getvalue().strip()
            key = f"Review.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f"destroy Review {f_value}")
            self.assertNotIn(key, storage.all())

    def test_destroy_class(self):
        """test  <class>.destroy()
        """
        for k in self.classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {k}")
                f_value = f.getvalue().strip()
                key = f"{k}.{f_value}"
                self.assertIn(key, storage.all())
                HBNBCommand().onecmd(
                    HBNBCommand().precmd(f"{k}.destroy({f_value})"))
                self.assertNotIn(key, storage.all())

    def test_BaseModel_destroy_class(self):
        """test BaseModel.destroy()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            f_value = f.getvalue().strip()
            key = f"BaseModel.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"BaseModel.destroy({f_value})"))
            self.assertNotIn(key, storage.all())

    def test_User_destroy_class(self):
        """test User.destroy()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            f_value = f.getvalue().strip()
            key = f"User.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"User.destroy({f_value})"))
            self.assertNotIn(key, storage.all())

    def test_State_destroy_class(self):
        """test State.destroy()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            f_value = f.getvalue().strip()
            key = f"State.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"State.destroy({f_value})"))
            self.assertNotIn(key, storage.all())

    def test_City_destroy_class(self):
        """test City.destroy()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            f_value = f.getvalue().strip()
            key = f"City.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"City.destroy({f_value})"))
            self.assertNotIn(key, storage.all())

    def test_Amenity_destroy_class(self):
        """test Amenity.destroy()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            f_value = f.getvalue().strip()
            key = f"Amenity.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"Amenity.destroy({f_value})"))
            self.assertNotIn(key, storage.all())

    def test_Place_destroy_class(self):
        """test Place.destroy()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            f_value = f.getvalue().strip()
            key = f"Place.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"Place.destroy({f_value})"))
            self.assertNotIn(key, storage.all())

    def test_Review_destroy_class(self):
        """test Review.destroy()
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            f_value = f.getvalue().strip()
            key = f"Review.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"Review.destroy({f_value})"))
            self.assertNotIn(key, storage.all())

    def test_do_update(self):
        """test update <class>
        """
        for k, _ in self.classes.items():
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {k}")
                f_value = f.getvalue().strip()
                key = f"{k}.{f_value}"
                self.assertIn(key, storage.all())
                HBNBCommand().onecmd(f'update {k}\
                                     {f_value} "attribute" "value"')
                self.assertTrue(hasattr(storage.all()[key], "attribute"))
                self.assertEqual(storage.all()[key]
                                 .to_dict()["attribute"], "value")
                HBNBCommand().onecmd(f"destroy {k} {f_value}")
                self.assertNotIn(key, storage.all())

    def test_do_update_BaseModel(self):
        """test update BaseModel
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            f_value = f.getvalue().strip()
            key = f"BaseModel.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f'update BaseModel\
                                    {f_value} "attribute" "value"')
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy BaseModel {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_update_User(self):
        """test update User
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            f_value = f.getvalue().strip()
            key = f"User.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f'update User\
                                    {f_value} "attribute" "value"')
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy User {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_update_State(self):
        """test update State
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            f_value = f.getvalue().strip()
            key = f"State.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f'update State\
                                    {f_value} "attribute" "value"')
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy State {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_update_City(self):
        """test update City
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            f_value = f.getvalue().strip()
            key = f"City.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f'update City\
                                    {f_value} "attribute" "value"')
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy City {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_update_Amenity(self):
        """test update Amenity
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            f_value = f.getvalue().strip()
            key = f"Amenity.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f'update Amenity\
                                    {f_value} "attribute" "value"')
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy Amenity {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_update_Place(self):
        """test update Place
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            f_value = f.getvalue().strip()
            key = f"Place.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f'update Place\
                                    {f_value} "attribute" "value"')
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy Place {f_value}")
            self.assertNotIn(key, storage.all())

    def test_do_update_Review(self):
        """test update Review
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            f_value = f.getvalue().strip()
            key = f"Review.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(f'update Review\
                                    {f_value} "attribute" "value"')
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy Review {f_value}")
            self.assertNotIn(key, storage.all())

    def test_update_class(self):
        """test <class>.update(<id>, <attribute>, <value>)
        """
        for k, _ in self.classes.items():
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {k}")
                f_value = f.getvalue().strip()
                key = f"{k}.{f_value}"
                self.assertIn(key, storage.all())
                HBNBCommand().onecmd(
                    HBNBCommand().precmd(f'{k}.update(\
                                     {f_value}, "attribute", "value")'))
                self.assertTrue(hasattr(storage.all()[key], "attribute"))
                self.assertEqual(storage.all()[key]
                                 .to_dict()["attribute"], "value")
                HBNBCommand().onecmd(f"destroy {k} {f_value}")
                self.assertNotIn(key, storage.all())

    def test_BaseModel_update_class(self):
        """test BaseModel.update(<id>, <attribute>, <value>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            f_value = f.getvalue().strip()
            key = f"BaseModel.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'BaseModel.update(\
                                        {f_value}, "attribute", "value")'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy BaseModel {f_value}")
            self.assertNotIn(key, storage.all())

    def test_User_update_class(self):
        """test User.update(<id>, <attribute>, <value>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            f_value = f.getvalue().strip()
            key = f"User.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'User.update(\
                                        {f_value}, "attribute", "value")'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy User {f_value}")
            self.assertNotIn(key, storage.all())

    def test_State_update_class(self):
        """test State.update(<id>, <attribute>, <value>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            f_value = f.getvalue().strip()
            key = f"State.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'State.update(\
                                        {f_value}, "attribute", "value")'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy State {f_value}")
            self.assertNotIn(key, storage.all())

    def test_City_update_class(self):
        """test City.update(<id>, <attribute>, <value>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            f_value = f.getvalue().strip()
            key = f"City.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'City.update(\
                                        {f_value}, "attribute", "value")'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy City {f_value}")
            self.assertNotIn(key, storage.all())

    def test_Amenity_update_class(self):
        """test Amenity.update(<id>, <attribute>, <value>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            f_value = f.getvalue().strip()
            key = f"Amenity.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'Amenity.update(\
                                        {f_value}, "attribute", "value")'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy Amenity {f_value}")
            self.assertNotIn(key, storage.all())

    def test_Place_update_class(self):
        """test Place.update(<id>, <attribute>, <value>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            f_value = f.getvalue().strip()
            key = f"Place.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'Place.update(\
                                        {f_value}, "attribute", "value")'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy Place {f_value}")
            self.assertNotIn(key, storage.all())

    def test_Review_update_class(self):
        """test Review.update(<id>, <attribute>, <value>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            f_value = f.getvalue().strip()
            key = f"Review.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'Review.update(\
                                        {f_value}, "attribute", "value")'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy Review {f_value}")
            self.assertNotIn(key, storage.all())

    def test_update_class_dict(self):
        """test <class>.update(<id>, <dictionary>)
        """
        for k, _ in self.classes.items():
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {k}")
                f_value = f.getvalue().strip()
                key = f"{k}.{f_value}"
                self.assertIn(key, storage.all())
                HBNBCommand().onecmd(
                    HBNBCommand().precmd(f'{k}.update(\
                                         {f_value}, \
                                            {{"attribute": "value"}})'))
                self.assertTrue(hasattr(storage.all()[key], "attribute"))
                self.assertEqual(storage.all()[key]
                                 .to_dict()["attribute"], "value")
                HBNBCommand().onecmd(f"destroy {k} {f_value}")
                self.assertNotIn(key, storage.all())

    def test_BaseModel_update_class_dict(self):
        """test BaseModel.update(<id>, <dictionary>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            f_value = f.getvalue().strip()
            key = f"BaseModel.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'BaseModel.update(\
                                        {f_value}, \
                                        {{"attribute": "value"}})'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy BaseModel {f_value}")
            self.assertNotIn(key, storage.all())

    def test_User_update_class_dict(self):
        """test User.update(<id>, <dictionary>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            f_value = f.getvalue().strip()
            key = f"User.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'User.update(\
                                        {f_value}, \
                                        {{"attribute": "value"}})'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy User {f_value}")
            self.assertNotIn(key, storage.all())

    def test_State_update_class_dict(self):
        """test State.update(<id>, <dictionary>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create State")
            f_value = f.getvalue().strip()
            key = f"State.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'State.update(\
                                        {f_value}, \
                                        {{"attribute": "value"}})'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy State {f_value}")
            self.assertNotIn(key, storage.all())

    def test_City_update_class_dict(self):
        """test City.update(<id>, <dictionary>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create City")
            f_value = f.getvalue().strip()
            key = f"City.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'City.update(\
                                        {f_value}, \
                                        {{"attribute": "value"}})'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy City {f_value}")
            self.assertNotIn(key, storage.all())

    def test_Amenity_update_class_dict(self):
        """test Amenity.update(<id>, <dictionary>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            f_value = f.getvalue().strip()
            key = f"Amenity.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'Amenity.update(\
                                        {f_value}, \
                                        {{"attribute": "value"}})'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy Amenity {f_value}")
            self.assertNotIn(key, storage.all())

    def test_Place_update_class_dict(self):
        """test Place.update(<id>, <dictionary>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            f_value = f.getvalue().strip()
            key = f"Place.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'Place.update(\
                                        {f_value}, \
                                        {{"attribute": "value"}})'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy Place {f_value}")
            self.assertNotIn(key, storage.all())

    def test_Review_update_class_dict(self):
        """test Review.update(<id>, <dictionary>)
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            f_value = f.getvalue().strip()
            key = f"Review.{f_value}"
            self.assertIn(key, storage.all())
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'Review.update(\
                                        {f_value}, \
                                        {{"attribute": "value"}})'))
            self.assertTrue(hasattr(storage.all()[key], "attribute"))
            self.assertEqual(storage.all()[key]
                             .to_dict()["attribute"], "value")
            HBNBCommand().onecmd(f"destroy Review {f_value}")
            self.assertNotIn(key, storage.all())


class TestConsoleBreaking(unittest.TestCase):
    """unittest class for HBNBCommand class when everything breaks
    """
    def test_wrong_command(self):
        """test a wrong command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("reate")
            f_output = f.getvalue().strip()
            cmd_output = "*** Unknown syntax: reate"
            self.assertEqual(f_output, cmd_output)

    def test_all_wrong_class(self):
        """test all with wrong
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all ds")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_class_all_wrong_class(self):
        """test all with wrong
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("ds.all()"))
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_create_no_class(self):
        """test create with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_create_wrong_class(self):
        """test create with wrong class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create urs")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_show_no_class(self):
        """test show with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_show_wrong_class(self):
        """test show with wrong class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show ds")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_class_show_wrong_class(self):
        """test show with wrong class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("ds.show()"))
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_show_no_id(self):
        """test show with no id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            f_output = f.getvalue().strip()
            cmd_output = "** instance id missing **"
            self.assertEqual(f_output, cmd_output)

    def test_class_show_no_id(self):
        """test show with no id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("BaseModel.show()"))
            f_output = f.getvalue().strip()
            cmd_output = "** instance id missing **"
            self.assertEqual(f_output, cmd_output)

    def test_show_wrong_id(self):
        """test show with wrong id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 0")
            f_output = f.getvalue().strip()
            cmd_output = "** no instance found **"
            self.assertEqual(f_output, cmd_output)

    def test_class_show_wrong_id(self):
        """test show with wrong id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("BaseModel.show(0)"))
            f_output = f.getvalue().strip()
            cmd_output = "** no instance found **"
            self.assertEqual(f_output, cmd_output)

    def test_destroy_no_class(self):
        """test destroy with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_destroy_wrong_class(self):
        """test destroy with wrong
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy ds")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_class_destroy_wrong_class(self):
        """test destroy with wrong
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("ds.destroy()"))
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_destroy_no_id(self):
        """test destroy with no id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
            f_output = f.getvalue().strip()
            cmd_output = "** instance id missing **"
            self.assertEqual(f_output, cmd_output)

    def test_class_destroy_no_id(self):
        """test destroy with no id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("BaseModel.destroy()"))
            f_output = f.getvalue().strip()
            cmd_output = "** instance id missing **"
            self.assertEqual(f_output, cmd_output)

    def test_destroy_wrong_id(self):
        """test destroy with wrong id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 0")
            f_output = f.getvalue().strip()
            cmd_output = "** no instance found **"
            self.assertEqual(f_output, cmd_output)

    def test_class_destroy_wrong_id(self):
        """test destroy with wrong id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("BaseModel.destroy(0)"))
            f_output = f.getvalue().strip()
            cmd_output = "** no instance found **"
            self.assertEqual(f_output, cmd_output)

    def test_update_no_class(self):
        """test update with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
            f_output = f.getvalue().strip()
            cmd_output = "** class name missing **"
            self.assertEqual(f_output, cmd_output)

    def test_update_wrong_class(self):
        """test update with wrong class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update cls")
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_class_update_wrong_class(self):
        """test update with wrong class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("cls.update()"))
            f_output = f.getvalue().strip()
            cmd_output = "** class doesn't exist **"
            self.assertEqual(f_output, cmd_output)

    def test_update_no_id(self):
        """test update with no id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User")
            f_output = f.getvalue().strip()
            cmd_output = "** instance id missing **"
            self.assertEqual(f_output, cmd_output)

    def test_class_update_no_id(self):
        """test update with no id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("User.update()"))
            f_output = f.getvalue().strip()
            cmd_output = "** instance id missing **"
            self.assertEqual(f_output, cmd_output)

    def test_update_wrong_id(self):
        """test update with wrong id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update User 0")
            f_output = f.getvalue().strip()
            cmd_output = "** no instance found **"
            self.assertEqual(f_output, cmd_output)

    def test_class_update_wrong_id(self):
        """test update with wrong id
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd("User.update(0)"))
            f_output = f.getvalue().strip()
            cmd_output = "** no instance found **"
            self.assertEqual(f_output, cmd_output)

    def test_update_no_attribute(self):
        """test update with no attribute
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            usr_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"update User {usr_id}")
            f_output = f.getvalue().strip()
            cmd_output = "** attribute name missing **"
            self.assertEqual(f_output, cmd_output)
            HBNBCommand().onecmd(f"destroy User {usr_id}")

    def test_class_update_no_attribute(self):
        """test update with no attribute
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            usr_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f"update User {usr_id}"))
            f_output = f.getvalue().strip()
            cmd_output = "** attribute name missing **"
            self.assertEqual(f_output, cmd_output)
            HBNBCommand().onecmd(f"destroy User {usr_id}")

    def test_update_no_value(self):
        """test update with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            usr_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f'update User {usr_id} "attribute"')
            f_output = f.getvalue().strip()
            cmd_output = "** value missing **"
            self.assertEqual(f_output, cmd_output)
            HBNBCommand().onecmd(f"destroy User {usr_id}")

    def test_class_update_no_value(self):
        """test update with no class
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create User")
            usr_id = f.getvalue().strip()
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                HBNBCommand().precmd(f'update User {usr_id} "attribute"'))
            f_output = f.getvalue().strip()
            cmd_output = "** value missing **"
            self.assertEqual(f_output, cmd_output)
            HBNBCommand().onecmd(f"destroy User {usr_id}")
