import math
import threading
import time

from discord_front_end.UserMessageResponder import UserMessageResponder
from discord_front_end.credits.CreditColumnDataGateway import CreditColumnDataGateway


class FixedTimeIntervalCostThread(threading.Thread):
    """
    Thread that constantly deducts credits from a guild's balance while it is running.

    The cost is specified on an hourly basis
    """

    def __init__(self, guild_id: int, hourly_cost: float, sleep_time: int, credit_data_gateway: CreditColumnDataGateway,
                 unregister_actions, responder: UserMessageResponder):
        """
        Creates a new thread that deducts credits from a guild's balance on an hourly basis
        :param guild_id: the guild of which to deduct
        :param hourly_cost: the amount of credits to deduct per hour
        :param sleep_time: the time to sleep between each deduction in seconds
        :param credit_manager: the credit manager to use for the deduction
        :param responder: the channel to send credit shortage notifications to the user
        """
        super().__init__()
        self.guild_id = guild_id
        self.hourly_cost = hourly_cost
        self.credit_data_gateway = credit_data_gateway
        self.active = True
        self.sleep_time = sleep_time
        self.start_time = None
        self.responder = responder

        # Hacky, but works: In case the task aborts, it has to unregister itself using this lambda
        self.unregister_function = unregister_actions

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

    def stop(self):
        """
        Stops the deduction thread
        """
        self.active = False

    def run(self):
        """
        Runs the thread
        """

        self.start_time = time.time()

        while self.active:
            balance = self.credit_data_gateway.get_credit_balance(self.guild_id)

            if balance < self.hourly_cost:
                self.handle_credits_running_out()
                continue

            self.credit_data_gateway.deduct_credits(self.guild_id, self.hourly_cost)

            # TODO only if balance is low
            self.responder.send_remote_message('credits_charge', None, [self.hourly_cost, balance - self.hourly_cost])
            self._notify_if_necessary()
            time.sleep(self.sleep_time)

    def handle_credits_running_out(self):
        """
        Handles the case when the user aborts the credit deduction
        """
        credit_balance = self.credit_data_gateway.get_credit_balance(self.guild_id)

        seconds_left = (credit_balance / self.hourly_cost) * self.sleep_time
        self.sleep_time = math.floor(seconds_left)

        minutes_left = math.floor(seconds_left / 60)
        remainder_seconds = seconds_left % 60
        self.responder.send_remote_message('credits_one_hour_notification', None, [minutes_left, remainder_seconds])

        time.sleep(self.sleep_time)

        # Only charge if the user has not stopped in the meantime or the user has more credits again
        credit_balance = self.credit_data_gateway.get_credit_balance(self.guild_id)
        if self.active and credit_balance < self.hourly_cost:
            self.stop()
            self.responder.send_remote_message('server_stopped_forced', None, [])
            actual_partial_cost = self.get_uptime() % self.sleep_time * self.hourly_cost
            cost = min(credit_balance, actual_partial_cost)  # Makes sure we don't deduct more than the balance
            self.credit_data_gateway.deduct_credits(self.guild_id, cost)
            self.unregister_function(self.guild_id)

    def _notify_if_necessary(self):
        """
        Notifies the user in multiple cases when they start to run low on credits.

        - Notify if user can only afford another 10 hours
        - Notify if user can only afford another 3 hours and give the precise shutdown time
        - Notify if user can only afford another 1 hour and give the precise shutdown time

        This is a hacky design choice to be fast. This should be extracted into observers on the credit balance.
        """
        pass
        # TODO