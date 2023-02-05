from discord_front_end.utils.db import MongoGateWay


class CreditColumnDataGateway:
    """
    Provides to the credit balance of a guild.

    Acts as a Column Data Gateway for the credit column in the instances document database.
    """

    def __init__(self, database_gateway: MongoGateWay):
        self.database_gateway = database_gateway

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