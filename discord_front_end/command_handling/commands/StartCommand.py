import threading

from discord_front_end.command_handling.Command import Command

"""
Command to start a game server.
"""
class StartCommand(Command):
    """
    Creates a new start command instance.

    Before this command can be executed, its arguments must be parsed into it.
    """
    def __init__(self):
        super().__init__("start")
        self.channel_id = None
        self.guild_id = None

    """
    Parses the arguments for this command from the provided argument string list and extracts relevant information form
    the discord message object.
        
    Expected arguments in the arguments: none.
    """
    def parse_arguments(self, arguments: list, discord_msg):
        self.guild_id = discord_msg.guild.id
        self.channel_id = discord_msg.channel.id

    """
    (See parent class)
    """
    def execute(self):
        print("Start command executed with {} arguments".format(self.guild_id))
        pass
