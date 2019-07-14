import sqlite3
from bank_bot.settings import TRANSACTION_MODEL_DATA

class Transaction(object):
    def __init__(
        self, sender_hash, recepient_hash, amount, transaction_hash, created_time=None
    ):
        self.sender_hash = sender_hash
        self.recepient_hash = recepient_hash
        self.amount = amount
        self.transaction_hash = transaction_hash
        self.created_time = created_time

    def __str__(self):
        return TRANSACTION_MODEL_DATA.substitute(
            sender_hash=self.sender_hash, reciever_hash=self.recepient_hash, 
            amount=self.amount, created=self.created_time, transaction_hash=self.transaction_hash
        )
        
    @classmethod
    def create_transaction(cls, sender_hash, recepient_hash, amount, database):
        return database.create_transaction(sender_hash, recepient_hash, amount)

    @classmethod
    def list_transactions(cls, user_hash, is_sender, database):
        return database.inspect_transactions(user_hash, is_sender, cls)

    @classmethod
    def list_all_transactions(cls, user_hash, database):
        return database.inspect_all_transactions(user_hash, cls)

    @classmethod
    def list_pair_history_transactions(cls, sender_hash, recepient_hash, database):
        return database.inspect_pair_history_transactions(sender_hash, recepient_hash, cls)