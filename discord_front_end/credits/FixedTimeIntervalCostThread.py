import threading
import time

from discord_front_end.credits.CreditManager import CreditManager


class FixedTimeIntervalCostThread(threading.Thread):
    """
    Thread that constantly deducts credits from a guild's balance while it is running.

    The cost is specified on an hourly basis
    """

    def __init__(self, guild_id: int, hourly_cost: float, sleep_time: int, credit_manager: CreditManager):
        """
        Creates a new thread that deducts credits from a guild's balance on an hourly basis
        :param guild_id: the guild of which to deduct
        :param hourly_cost: the amount of credits to deduct per hour
        :param sleep_time: the time to sleep between each deduction in seconds
        :param credit_manager: the credit manager to use for the deduction
        """
        super().__init__()
        self.guild_id = guild_id
        self.hourly_cost = hourly_cost
        self.credit_manager = credit_manager
        self.active = True
        self.sleep_time = sleep_time
        self.start_time = None

    def run(self):
        """
        Runs the thread
        """

        self.start_time = time.time()

        while self.active:
            time.sleep(self.sleep_time)
            self.credit_manager.deduct_credits(self.guild_id, self.hourly_cost)

    def stop(self):
        """
        Stops the deduction thread
        """
        self.active = False

    def get_uptime(self) -> int:
        """
        Returns the uptime of the thread
        :return: the uptime of the thread in seconds. -1 if the thread has not started yet
        """
        if self.start_time is None:
            return -1

        return time.time() - self.start_time

    def get_hourly_cost(self) -> float:
        """
        Returns the hourly cost of the thread
        :return: the hourly cost of the thread
        """

        return self.hourly_cost
