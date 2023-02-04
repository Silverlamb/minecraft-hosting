import asyncio

from discord_front_end.UserMessageResponder import UserMessageResponder
from discord_front_end.credits.CreditColumnDataGateway import CreditColumnDataGateway
from discord_front_end.credits.FixedTimeIntervalCostThread import FixedTimeIntervalCostThread


class CreditManager:
    """
    Affords starting and stopping deduction of credits on hourly basis.

    It includes some business logic for using this credit information in order to do the deduction. This is a design
    compromise chosen to accelerate implementation.
    """

    def __init__(self, credit_column_data_gateway: CreditColumnDataGateway):
        self.credit_column_data_gateway = credit_column_data_gateway

        # Map of guild_id to credit deduction task, if there is a credit deduction task running for that guild
        self.credit_deduction_task = {}
        self.deduction_sleep_time = 3600

    def start_deduction(self, guild_id: int, hourly_cost: float, responder: UserMessageResponder) -> None:
        """
        Starts a task that deducts credits from the credit balance of a guild on an hourly basis.

        Checks whether the user has enough credits to pay for the first interval. If not, the task is not started and
        an exception is raised.

        :param guild_id: the guild of which to deduct
        :param hourly_cost: the amount of credits to deduct per hour
        :param responder: the channel to use to follow up with notifications on this running server. It must have the
                          default channel id set, as this is where the notifications will be sent to.
                          E.g. used to send credit shortage notifications to the user
        """
        if guild_id in self.credit_deduction_task:
            raise Exception("There already is a credit deduction task already running for guild {}".format(guild_id))

        if not self.credit_column_data_gateway.can_afford(guild_id, hourly_cost):
            balance = self.credit_column_data_gateway.get_credit_balance(guild_id)
            raise Exception("Your credits ({}) are not sufficient to pay the first interval.".format(balance))

        self.credit_deduction_task[guild_id] = FixedTimeIntervalCostThread(guild_id, hourly_cost,
                                                                           self.deduction_sleep_time, self, responder)
        self.credit_deduction_task[guild_id].start()

    def stop_deduction(self, guild_id: int) -> None:
        """
        Stops the task that deducts credits from the credit balance of a guild on an hourly basis
        """
        if guild_id not in self.credit_deduction_task:
            raise Exception("There is no credit deduction task running for guild {}".format(guild_id))

        self.credit_deduction_task[guild_id].stop()
        uptime = self.credit_deduction_task[guild_id].get_uptime()
        del self.credit_deduction_task[guild_id]

        # Deduct the cost for the last interval that was not finished
        not_used_seconds = self.deduction_sleep_time - (uptime % self.deduction_sleep_time)
        not_used_cost = (not_used_seconds / self.deduction_sleep_time) * \
                          self.credit_deduction_task[guild_id].get_hourly_cost()
        self.credit_column_data_gateway.add_credits(guild_id, not_used_cost)
