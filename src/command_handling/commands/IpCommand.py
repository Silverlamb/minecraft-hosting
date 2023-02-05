import threading

from UserMessageResponder import UserMessageResponder
from command_handling.commands.ServerCommand import ServerCommand
from utils.mongo_gateway import MongoGateway
from utils.instance_manager import InstanceManager


class IpCommand(ServerCommand):
    """
    Command to get the ip of a game server.
    """

    def __init__(self, responder: UserMessageResponder, database_gateway: MongoGateway, server_manager: InstanceManager):
        """Creates a new ip command instance.

        Before this command can be executed, its arguments must be parsed into it.
        """
        super().__init__("ip", responder, database_gateway, server_manager)
        self.discord_msg = None

    def __copy__(self):
        """
        (See parent class)
        """
        return IpCommand(self.responder, self.database_gateway, self.server_manager)

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

        instance_data = self.database_gateway.find_instance_one(self.discord_msg.guild.id)
        ip_string = instance_data['ip']

        if ip_string == '':
            raise Exception("You must start the server before you can get the IP address! Run '!server start.'")
        else:
            self.responder.send_remote_message('print_ip', self.discord_msg.channel.id, [ip_string])


