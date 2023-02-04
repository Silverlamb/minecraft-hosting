from abc import abstractmethod

"""
Abstract class that represents a general command.

A command must be executable with through its 'execute()' method.
Every concrete command class has a constructor that takes the commands arguments as a string array and parses them.
"""


class Command:

    """
    Abstract constructor for a command. Should not be called from outside a constructor of a concrete command class.

    Specifies the name of the command.
    """
    def __init__(self, name: str):
        self.name = name

    """
    Executes the command.

    Usually, one command object will only be executed once.
    """

    @abstractmethod
    def execute(self):
        pass

    """
    Returns the name of this command.
    
    Should usually be a single lowercase word.
    """

    def get_name(self) -> str:
        return self.name

