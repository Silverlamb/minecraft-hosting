from abc import abstractmethod, ABC

"""
Abstract class that represents a general command.

A command must be executable with through its 'execute()' method.
Its arguments must be parsed through its 'parse_arguments()' method before executing the command.
"""


class Command(ABC):

    """
    Abstract constructor for a command. Should not be called from outside a constructor of a concrete command class.

    Specifies the name of the command.
    """
    def __init__(self, name: str):
        self.name = name

    """
    Takes the commands arguments as a string array and parses them.
    Additionally, the discord message object is passed to the command to provide additional information like the author.
    """
    @abstractmethod
    def parse_arguments(self, arguments: list, discord_msg) -> None:
        pass


    """
    Executes the command.

    Every subclass must call this method via super first, before executing its own logic in their execute() method.
    
    Usually, one command object will only be executed once.
    """

    @abstractmethod
    def execute(self) -> None:
        pass

    """
    Returns a shallow copy of this command object.
    """
    def __copy__(self):
        return Command(self.name)

    """
    Returns the name of this command.
    
    Should usually be a single lowercase word.
    """

    def get_name(self) -> str:
        return self.name

