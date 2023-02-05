import threading

from UserMessageResponder import UserMessageResponder
from command_handling.commands.ServerAdminCommand import ServerAdminCommand
from command_handling.commands.ServerCommand import ServerCommand
from utils.mongo_gateway import MongoGateway
from utils.instance_manager import InstanceManager


class DestroyCommand(ServerAdminCommand):
    """
    Command to stop a game server.
    """

    def __init__(self, responder: UserMessageResponder, database_gateway: MongoGateway, server_manager: InstanceManager):
        """Creates a new destroy command instance.

        Before this command can be executed, its arguments must be parsed into it.
        """
        super().__init__("destroy", responder, database_gateway, server_manager)
        self.discord_msg = None

    def __copy__(self):
        """
        (See parent class)
        """
        return DestroyCommand(self.responder, self.database_gateway, self.server_manager)

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

        threading.Thread(target=self.server_manager.server_destroy, args=(self.discord_msg.guild.id
                                                                            )).start()


