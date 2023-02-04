import asyncio

from discord_front_end.UserMessageResponder import UserMessageResponder
from discord_front_end.credits.FixedTimeIntervalCostThread import FixedTimeIntervalCostThread
from discord_front_end.utils.db import MongoGateWay


class CreditManager:
    """
    Provides to the credit balance of a guild and affords starting and stopping deduction of credits on hourly basis.

    Acts as a Column Data Gateway for the credit column in the instances document database. Additionally, it
    includes some business logic for using this credit information in order to do the deduction. This is a design
    compromise chosen to accelerate implementation.
    """

    def __init__(self, database_gateway: MongoGateWay):
        self.database_gateway = database_gateway

        # Map of guild_id to credit deduction task, if there is a credit deduction task running for that guild
        self.credit_deduction_task = {}
        self.deduction_sleep_time = 3600

    def get_credit_balance(self, guild_id: int) -> float:
        """
        Returns the credit balance of a guild
        """
        return self.database_gateway.find_instance_one(guild_id)["credits"]

    def can_afford(self, guild_id: int, amount: float) -> bool:
        """
        Returns whether a guild can afford a certain amount of credits.

        Convenience method for get_credit_balance(guild_id)
        """
        return self.get_credit_balance(guild_id) >= amount

    def add_credits(self, guild_id: int, credits: float) -> None:
        """
        Adds credits to the credit balance of a guild
        """
        self.database_gateway.update_instance_one(guild_id, {"credits": self.get_credit_balance(guild_id) + credits})

    def deduct_credits(self, guild_id: int, credits: float) -> None:
        """
        Deducts credits from the credit balance of a guild
        """
        self.database_gateway.update_instance_one(guild_id, {"credits": self.get_credit_balance(guild_id) - credits})

    def start_deduction(self, guild_id: int, hourly_cost: float, responder: UserMessageResponder) -> None:
        """
        Starts a task that deducts credits from the credit balance of a guild on an hourly basis

        :param guild_id: the guild of which to deduct
        :param hourly_cost: the amount of credits to deduct per hour
        :param responder: the channel to use to follow up with notifications on this running server.
                          E.g. used to send credit shortage notifications to the user
        """
        if guild_id in self.credit_deduction_task:
            raise Exception("There already is a credit deduction task already running for guild {}".format(guild_id))

        self.credit_deduction_task[guild_id] = FixedTimeIntervalCostThread(guild_id, hourly_cost,
                                                                           self.deduction_sleep_time, self)
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
        not_billed_seconds = uptime % self.deduction_sleep_time
        not_billed_cost = (not_billed_seconds / self.deduction_sleep_time) * \
                          self.credit_deduction_task[guild_id].get_hourly_cost()
        self.deduct_credits(guild_id, not_billed_cost)
