# AirBnB_clone

## Table of Contents
* [Description](#description)
* [Prerequisites](#prerequisites)
* [How to start it](#how-to-start-it)
* [How to use it](#how-to-use-it)
* [Examples of use](#examples-of-use)
* [Authors](#authors)
* [License](#license)


## Description
This project is the first step towards building our first full web application: an AirBnB clone.

In this iteration, we implement a backend in the form of a custom command-line interface for data management, and the base classes for the storage of this data. The application is built using Python.

The main purpose of the project is to prepare a user-friendly interface for managing properties and attributes of classes within the Airbnb clone environment.

The features currently implemented are:
- A Command Interpreter to manipulate and store data:
    - create a new object (ex: a new User or a new Place)
    - retrieve an object from a file, a database etc...
    - do operations on objects (count, compute stats, etc...)
    - update attributes of an object
    - destroy an object
- A storage engine implementing a simple flow of serialization/deserialization: 
    - instance <-> Dictionary <-> JSON string <-> file
    - creating classes to be used for the AirBnb platform (User, State, City, Place, Amenity, Review) that will later be integrated into the database system.
    - The file storage is an abstracted storage engine of the project.

## The console
The console was built using python's cmd.Cmd class. The cmd module provides the basic framework for creating line-oriented command interpreters. It is often used for test harnessing, because it allows you to simulate input at a command line. It provides administrative tools and fast prototyping capability to later be wrapped in a more sophisticated GUI.

## Prerequisites
You need to have Python3 installed on your computer.
If you don't have Python3 installed, you can refer to the instructions [here](https://github.com/mo7amedElfadil/alx-higher_level_programming/blob/main/README.md).

The only module you will need to install separately is pep8, which is used to check for the PEP8 coding style. To install from your terminal, run:
```bash
pip3 install pep8
```

Once you have them installed, you can clone the repository to your local machine by running the following command in your terminal:
```bash
git clone https://github.com/mo7amedElfadil/AirBnB_clone.git
```

## How to start it
Change your directory to the AirBnB_clone directory:
```bash
cd AirBnB_clone
```
Run the console.py file:
```bash
./console.py
# or
python3 console.py
```
and then you can try out the different commands, outlined in the next section.

## How to use it
The commands available in the console are:
- `create`: Creates a new instance of a class
- `show`: Prints the string representation of an instance based on the class name and id
- `destroy`: Deletes an instance based on the class name and id
- `all`: Prints all string representation of all instances based or not on the class name
- `update`: Updates an instance based on the class name and id by adding or updating attribute
- `quit`: Exits the program. Ctrl + D (on unix) or Ctrl + Z (on windows) also works

Each command is followed by its arguments separated by spaces. The following is a list of the commands and their arguments:
- `create <class name>`
- `show <class name> <id>`
- `destroy <class name> <id>`
- `all`
- `all <class name>`
- `update <class name> <id> <attribute name> "<attribute value>"`
- `quit`

 There is an alternative way of running the commands:
- `<class name>.all()`
- `<class name>.count()`
- `<class name>.show(<id>)`
- `<class name>.destroy(<id>)`
- `<class name>.update(<id>, <attribute name>, <attribute value>)`
- `<class name>.update(<id>, <dictionary representation>)`

For more information on the usage, refer to the documentation by typing:
```bash
(hbnb) help
# or
(hbnb) help <command>
# eg
(hbnb) help create
Create a new instance of a class, save it, print its id
        Ex:
        $ create BaseModel
        $ <class name>.create()
        $ User.create()
```

## Examples of use
The console works like this in interactive mode:
```bash
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) all
["[User] (2bdc06cf-fd24-4474-9187-99019e88da0d) {'id': '2bdc06cf-fd24-4474-9187-99019e88da0d', 'created_at': datetime.datetime(2024, 1, 13, 17, 59, 16, 666440), 'updated_at': datetime.datetime(2024, 1, 13, 17, 59, 16, 666440)}", "[User] (b2a1d4be-36bb-4cd1-8c66-f444b4e62c2d) {'id': 'b2a1d4be-36bb-4cd1-8c66-f444b4e62c2d', 'created_at': datetime.datetime(2024, 1, 13, 17, 59, 19, 804170), 'updated_at': datetime.datetime(2024, 1, 13, 17, 59, 19, 804170)}", "[User] (fd1e76d6-d5c8-4a8b-9985-61e75e073ff9) {'id': 'fd1e76d6-d5c8-4a8b-9985-61e75e073ff9', 'created_at': datetime.datetime(2024, 1, 13, 18, 51, 26, 27822), 'updated_at': datetime.datetime(2024, 1, 13, 18, 51, 26, 27822)}"]
(hbnb) create User
dcba6e55-5068-4324-9de2-656a8fa405e0
(hbnb) show User dcba6e55-5068-4324-9de2-656a8fa405e0
[User] (dcba6e55-5068-4324-9de2-656a8fa405e0) {'id': 'dcba6e55-5068-4324-9de2-656a8fa405e0', 'created_at': datetime.datetime(2024, 1, 13, 22, 22, 10, 992029), 'updated_at': datetime.datetime(2024, 1, 13, 22, 22, 10, 992029)}
(hbnb) update User dcba6e55-5068-4324-9de2-656a8fa405e0 first_name "John"
(hbnb) show User dcba6e55-5068-4324-9de2-656a8fa405e0
[User] (dcba6e55-5068-4324-9de2-656a8fa405e0) {'id': 'dcba6e55-5068-4324-9de2-656a8fa405e0', 'created_at': datetime.datetime(2024, 1, 13, 22, 22, 10, 992029), 'updated_at': datetime.datetime(2024, 1, 13, 22, 22, 10, 992029), 'first_name': 'John'}
(hbnb) User.update(dcba6e55-5068-4324-9de2-656a8fa405e0, "last_name", "Doe")
(hbnb) show User dcba6e55-5068-4324-9de2-656a8fa405e0
[User] (dcba6e55-5068-4324-9de2-656a8fa405e0) {'id': 'dcba6e55-5068-4324-9de2-656a8fa405e0', 'created_at': datetime.datetime(2024, 1, 13, 22, 22, 10, 992029), 'updated_at': datetime.datetime(2024, 1, 13, 22, 22, 10, 992029), 'first_name': 'John', 'last_name': 'Doe'}
(hbnb) destroy User dcba6e55-5068-4324-9de2-656a8fa405e0
(hbnb) show User dcba6e55-5068-4324-9de2-656a8fa405e0    
** no instance found **
(hbnb) quit
```

## Authors
This project was created by:
- [@mo7amedelfadil](https://github.com/mo7amedelfadil)
- [@sixthson6](https://github.com/sixthson6)

## License
Copyright © 2024 [MIT](LICENSE).


