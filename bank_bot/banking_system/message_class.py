import sqlite3
from bank_bot.settings import MESSAGE_MODEL_DATA

class Message(object):
    def __init__(
        self, sender_hash, recepient_hash, message_text, message_hash, created_time=None
    ):
        self.sender_hash = sender_hash
        self.recepient_hash = recepient_hash
        self.message_text = message_text
        self.created_time = created_time

    def __str__(self):
        return MESSAGE_MODEL_DATA.substitute(
            sender_hash=self.sender_hash, reciever_hash=self.recepient_hash, 
            message_text=self.message_text, created=self.created_time,
        )
        
    @classmethod
    def create_message(cls, sender_hash, recepient_hash, message_text, database):
        return database.create_message(sender_hash, recepient_hash, message_text)

    @classmethod
    def inspect_messages(cls, user_hash, is_sender, database):
        return database.inspect_messages(user_hash, is_sender, cls)

    @classmethod
    def inspect_all_messages(cls, user_hash, database):
        return database.inspect_all_messages(user_hash, cls)

    @classmethod
    def inspect_pair_history_messages(cls, sender_hash, recepient_hash, database):
        return database.inspect_pair_history_messages(sender_hash, recepient_hash, cls)
