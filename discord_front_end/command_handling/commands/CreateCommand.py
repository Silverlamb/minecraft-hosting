import threading

from discord_front_end.command_handling.commands.ServerCommand import ServerCommand
from discord_front_end.utils.db import MongoGateWay

"""
Command to create a game server.
"""
class CreateCommand(ServerCommand):

    """
    Creates a new create command instance.

    Before this command can be executed, its arguments must be parsed into it.
    """

    def __init__(self, database_gateway: MongoGateWay):
        super().__init__("create", database_gateway)
        self.discord_msg = None

    """
    Parses the arguments for this command from the provided argument string list and extracts relevant information form
    the discord message object.

    Expected arguments in the string arguments list: none.
    """
    def parse_arguments(self, arguments: list, discord_msg) -> None:
        self.discord_msg = discord_msg

    """
    (See parent class)
    """
    def execute(self) -> None:
        super().execute()
        threading.Thread(target=self._create_server,
                         args=(self.discord_msg.guild.id, self.discord_msg.channel.id)).start()

    """
    Starts a server based on guild id
    """
    def _create_server(self, guild_id, channel_id) -> None:
        pass
        # TODO
