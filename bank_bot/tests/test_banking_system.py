import sqlite3
from bank_bot.banking_system.client_factory import BankingClientFactory
from bank_bot.banking_system.banking_system_class_based import BankingClient

class MockMessage(object):
    def __init__(self, from_who, chat_id, message_text):
        self.json = {"from": {"id": from_who}, "chat": {"id": chat_id}}
        self.text = message_text

def test_client_creation(database):
    message = MockMessage(1, 2, "Mock")
    client = BankingClientFactory(database).create_client(message)
    assert isinstance(client, BankingClient)
    assert client.user_id == "1"
    assert client.chat_id == "2"
    assert client.user is None

