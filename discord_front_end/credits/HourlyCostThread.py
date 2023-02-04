import threading

from discord_front_end.credits.CreditManager import CreditManager


class HourlyCostThread(threading.Thread):
    """
    Thread that constantly deducts credits from a guild's balance while it is running.

    The cost is specified on an hourly basis
    """
    def __init__(self, guild_id: int, hourly_cost: float, credit_manager: CreditManager):
        super().__init__()
        self.guild_id = guild_id
        self.hourly_cost = hourly_cost
        self.credit_manager = credit_manager
        self.active = True

    def run(self):
        while self.active:
            self.credit_manager.deduct_credits(self.guild_id, self.hourly_cost)
            time.sleep(3600)

    def stop(self):
        self.active = False