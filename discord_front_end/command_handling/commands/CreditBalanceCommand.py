import threading

from discord_front_end.UserMessageResponder import UserMessageResponder
from discord_front_end.command_handling.Command import Command
from discord_front_end.command_handling.commands.ServerCommand import ServerCommand
from discord_front_end.credits.CreditColumnDataGateway import CreditColumnDataGateway
from discord_front_end.utils.db import MongoGateWay


class CreditBalanceCommand(Command):
    """
    Command to get the current balance of a guild.
    """

    def __init__(self, responder: UserMessageResponder, credit_data_gateway: CreditColumnDataGateway):
        """Creates a new ip command instance.

        Before this command can be executed, its arguments must be parsed into it.
        """
        super().__init__("credit balance", responder)
        self.discord_msg = None
        self.credit_data_gateway = credit_data_gateway

    def __copy__(self):
        """
        (See parent class)
        """
        return CreditBalanceCommand(self.responder, self.credit_data_gateway)

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

        balance = self.credit_data_gateway.get_credit_balance(self.discord_msg.guild.id)
        self.responder.send_remote_message('current_balance', self.discord_msg.channel.id, [balance])


