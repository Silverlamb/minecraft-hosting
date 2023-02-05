import threading

from UserMessageResponder import UserMessageResponder
from command_handling.commands.ServerAdminCommand import ServerAdminCommand
from command_handling.commands.ServerCommand import ServerCommand
from credits.CreditManager import CreditManager
from utils.mongo_gateway import MongoGateway
from utils.instance_manager import InstanceManager


class StopCommand(ServerAdminCommand):
    """
    Command to stop a game server.
    """

    def __init__(self, responder: UserMessageResponder, database_gateway: MongoGateway, server_manager: InstanceManager, credit_manager: CreditManager):
        """Creates a new stop command instance.

        Before this command can be executed, its arguments must be parsed into it.
        """
        super().__init__("stop", responder, database_gateway, server_manager)
        self.discord_msg = None
        self.credit_manager = credit_manager

    def __copy__(self):
        """
        (See parent class)
        """
        return StopCommand(self.responder, self.database_gateway, self.credit_manager)

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

        threading.Thread(target=self.server_manager.server_stop, args=(self.discord_msg.guild.id, 
                                                                         self.discord_msg.channel.id, 
                                                                         self.responder
                                                                         )).start()

        self.credit_manager.stop_deduction(self.discord_msg.guild.id)


