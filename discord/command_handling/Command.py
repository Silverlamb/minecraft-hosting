from abc import abstractmethod

"""
Abstract class that represents a general command.

A command must be executable with through its 'execute()' method.
Every concrete command class has a constructor that takes the commands arguments as a string array and parses them.
"""
class Command:

    """
    Executes the command.

    Usually, one command object will only be executed once.
    """
    @abstractmethod
    def execute(self):
        pass
