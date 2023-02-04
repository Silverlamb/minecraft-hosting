import threading

from discord_front_end.UserMessageResponder import UserMessageResponder
from discord_front_end.command_handling.commands.ServerCommand import ServerCommand
from discord_front_end.utils.db import MongoGateWay


class StopCommand(ServerCommand):
    """
    Command to stop a game server.
    """

    def __init__(self, responder: UserMessageResponder, database_gateway: MongoGateWay):
        """Creates a new stop command instance.

        Before this command can be executed, its arguments must be parsed into it.
        """
        super().__init__("stop", responder, database_gateway)
        self.discord_msg = None

    def __copy__(self):
        """
        (See parent class)
        """
        return StopCommand(self.responder, self.database_gateway)

    def parse_arguments(self, arguments: list, discord_msg) -> None:
        """
        Parses the arguments for this command from the provided argument string list and extracts relevant information
        from the discord message object.

        Expected arguments in the string arguments list: none.
        """
        self.discord_msg = discord_msg

    def execute(self) -> None:
        """
        (See parent class)
        """
        super().execute()

        # TODO Check whether user has sufficient credits

        threading.Thread(target=None, # TODO link stop backend
                         args=(self.discord_msg.guild.id, self.discord_msg.channel.id)).start()


