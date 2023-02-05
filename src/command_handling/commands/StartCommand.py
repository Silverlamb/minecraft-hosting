import copy
import threading

from UserMessageResponder import UserMessageResponder
from command_handling.commands.ServerAdminCommand import ServerAdminCommand
from credits.CreditManager import CreditManager
from utils.mongo_gateway import MongoGateway
from utils.instance_manager import InstanceManager


class StartCommand(ServerAdminCommand):
    """
    Command to start a game server.
    """

    HOURLY_CREDIT_DEDUCTION = 60

    def __init__(self, responder: UserMessageResponder, database_gateway: MongoGateway, server_manager: InstanceManager, credit_manager: CreditManager):
        """Creates a new start command instance.

        Before this command can be executed, its arguments must be parsed into it.
        """
        super().__init__("start", responder, database_gateway, server_manager)
        self.discord_msg = None
        self.credit_manager = credit_manager

    def __copy__(self):
        """
        (See parent class)
        """
        return StartCommand(self.responder, self.database_gateway, self.server_manager, self.credit_manager)

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

        # TODO Hacky solution: The check - whether starting is allowed - should be extracted to command-level and
        # thus wrapped around both the call to credit manager and the instance manager
        instance_data = self.database_gateway.find_instance_one(self.discord_msg.guild_id)
        if instance_data["server_state"] and not instance_data["server_present"] and not instance_data["is_process"]:
            defaulted_responder = self.responder.copy_with_default_channel_id(self.discord_msg.channel.id)
            self.credit_manager.start_deduction(self.discord_msg.guild.id, StartCommand.HOURLY_CREDIT_DEDUCTION,
                                                defaulted_responder)

        threading.Thread(target=self.server_manager.server_start, args=(self.discord_msg.guild.id, 
                                                                         self.discord_msg.channel.id, 
                                                                         self.responder
                                                                         )).start()
