#!/usr/bin/python3
"""
Entry point into the AirBnB console app
"""
import cmd
import models
from models.base_model import BaseModel
# from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """AirBnB CLI
    Commands:
    quit, EOF, help
    """
    prompt = "(hbnb) "
    class_name = {'BaseModel': BaseModel}

    # pylint: disable-next=unused-argument
    def do_quit(self, arg) -> bool:
        """Quit command to exit the program
        """
        return True

    def do_create(self, arg):
        """
        create command to create new instance of BaseModel
        and save it as a json file
        """
        if not arg:
            print("** class name is missing **")
        elif arg not in self.class_name.keys():
            print("** class doesn't exit **")
        else:
            new_instance = self.class_name[arg]()
            # new_instance.to_json()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Show command to print the str representation of an instance
        based on class name and id
        """
        argts = arg.split()
        if not arg:
            print("** class name missing **")
            return
        elif argts[0] != "BaseModel":
            print("** class doesn't exit **")
        elif len(argts) < 2:
            print("** instance id is missing **")
        elif argts[0]+"."+argts[1] not in\
                models.storage._FileStorage__objects.keys():
                    print("** no instance found **")
        else:
            new_instance = models.storage.all()[argts[0]+"."+argts[1]]
            print(new_instance)

    def do_destroy(self, arg):
        """Destroy command to delete instances specified
        based on class name and id
        """
        argts = arg.split()
        if not arg:
            print("** class name missing **")
            return
        if argts[0] not in self.class_name.keys():
            print("** class doesn't exist **")
        elif len(argts) == 1:
            print("** instance id missing **")
        elif argts[0]+"."+argts[1] not in\
                models.storage._FileStorage__objects.keys():
                    print("** no instance found **")
        else:
            del models.storage._FileStorage__objects[argts[0]+"."+argts[1]]
            models.storage.save()

    def do_all(self, arg):
        """All command to print all string representatio of
        every instance based on class name or no class name
        """
        all_cls = []
        if arg and arg not in self.class_name.keys():
            print("** class doesnt exist **")
            return
        for cls in models.storage._FileStorage__objects.keys():
            all_cls.append(models.storage._FileStorage__objects[cls].__str__())

        print('["{}"]'.format(", ".join(all_cls)))

    def do_update(self, arg):
        """Update command to update an instance
        based on the class name and id
        adding or updating the attribute
        """
        if not arg:
            print("** class name is missing **")
            return
        argts = arg.split()
        if argts[0] not in self.class_name.keys():
            print("** class doesn't exist **")
        elif len(argts) == 1:
            print("** instance id missing **")
        elif argts[0]+"."+argts[1] not in\
                models.storage._FileStorage__objects.keys():
                    print("** no instance found **")
        elif len(argts) == 2:
            print("** attribute name missing **")
        elif len(argts) == 3:
            print("** value missing **")
        else:
            instance = models.storage.all()[argts[0]+"."+argts[1]]
            attr = argts[2]
            val = argts[3]
            setattr(instance, attr, val)
            instance.save()
            models.storage.save()

        

    do_EOF = do_quit


if __name__ == "__main__":
    HBNBCommand().cmdloop()
