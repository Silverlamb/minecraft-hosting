from command_handling.Command import Command

"""
For a given command string, creates the appropriate command objects and gives them the necessary arguments.
"""
class CommandParser:
    def __init__(self):
        # List of the commands that this parser can parse
        self.command_list = []
        pass

    """
    Takes a command string and creates 
    """
    def parse_command(self, command_string: str) -> Command:
        string_elements = command_string.split(" ")
        for command in self.command_list:
            if command.get_name() == string_elements[0]:
                return command(string_elements[1:])


