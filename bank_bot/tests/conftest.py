import os
import pytest
from bank_bot.banking_system import Database

class MockMessage(object):
    def __init__(self, from_who, chat_id, message_text):
        self.json = {"from": {"id": from_who}, "chat": {"id": chat_id}}
        self.text = message_text

@pytest.fixture
def database():
    test_file_path = "test_database.db"
    database = Database(test_file_path)
    database.initialize_system()
    yield database
    os.remove(test_file_path)

@pytest.fixture
def mock_message():
    message = MockMessage(2, 2, "Mock")
    return message
