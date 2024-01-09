#!/usr/bin/python3
"""
Entry point into the AirBnB console app
"""
import cmd
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """AirBnB CLI
    Commands:
    quit, EOF, help
    """
    prompt = "(hbnb) "

    _models = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
        }
    str_attr = ["name", "amenity_id", "place_id", "state_id",
                "user_id", "city_id", "description", "text",
                "email", "password", "first_name", "last_name"]
    int_attr = ["number_rooms", "number_bathrooms",
                "max_guest", "price_by_night"]
    float_attr = ["latitude", "longitude"]

    # pylint: disable-next=unused-argument
    def do_quit(self, arg) -> bool:
        """Quit command to exit the program
        """
        return True

    do_EOF = do_quit

    def do_create(self, arg) -> None:
        """Create a new instance of a class, save it, print its id
        Ex:
        $ create BaseModel
        """
        args = arg.split()
        if not self.validate_cls(args):
            return
        instance = self._models[args[0]]()
        storage.save()
        print(instance.id)

    def do_show(self, arg) -> None:
        """Prints the string representation of an instance
        based on the class name and id
        Ex:
        $ show BaseModel 1234-1234-1234
        """
        args = arg.split()
        if not (self.validate_cls(args) and self.validate_id(args)):
            return
        print(storage.all()[args[0] + "." + args[1]])

    def do_destroy(self, arg) -> None:
        """Deletes an instance based on the class name and id
        (save the change into the JSON file)
        Ex:
        $ destroy BaseModel 1234-1234-1234
        """
        args = arg.split()
        if not (self.validate_cls(args) and self.validate_id(args)):
            return
        del storage.all()[args[0] + "." + args[1]]
        storage.save()

    def do_all(self, arg) -> None:
        """Prints all string representation of all instances
        based or not on the class name
        Ex:
        $ all BaseModel
        or
        $ all
        """
        args = arg.split()
        res = []
        if len(args) > 0:
            for k, v in storage.all().items():
                if args[0] == k.split(".")[0]:
                    res.append(str(v))
        else:
            for k, v in storage.all().items():
                res.append(str(v))
        print(res)

    def do_update(self, arg) -> None:
        """Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).
        update <class name> <id> <attribute name> "<attribute value>"
        Ex:
        $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        args = arg.split()
        if not (self.validate_cls(args) and self.validate_id(args)):
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        if args[3].startswith(("'", '"')) and args[3].endswith(("'", '"')):
            match = re.match(r"[\'\"](.*?)[\'\"]", arg[3]).group(1)
        else:
            match = arg[3]
        if args[2] in self.int_attr:
            setattr(storage.all()[args[0] + "." + args[1]],
                    args[2], int(match))
        elif args[2] in self.str_attr:
            setattr(storage.all()[args[0] + "." + args[1]],
                    args[2], str(match))
        elif args[2] in self.float_attr:
            setattr(storage.all()[args[0] + "." + args[1]],
                    args[2], float(match))
        else:
            setattr(storage.all()[args[0] + "." + args[1]],
                    args[2], self.type_cast(match))
        storage.save()

    def type_cast(self, arg) -> (float | int | str):
        """determine type of arg and cast it
        """
        try:
            if "." in arg:
                return float(arg)
            return int(arg)
        except ValueError:
            return arg

    def validate_cls(self, args) -> bool:
        """validate class creation
        """
        if len(args) < 1:
            print("** class name missing **")
            return False
        if args[0] not in self._models:
            print("** class doesn't exist **")
            return False
        return True

    def validate_id(self, args) -> bool:
        """validate id of class instance
        """
        if len(args) < 2:
            print("** instance id missing **")
            return False
        instance_id = args[0] + "." + args[1]
        if instance_id not in storage.all():
            print("** no instance found **")
            return False
        return True


if __name__ == "__main__":
    HBNBCommand().cmdloop()
