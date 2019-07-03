import os
import pytest
from bank_bot.banking_system import Database

@pytest.fixture
def database():
    test_file_path = "test_database.db"
    database = Database(test_file_path)
    database.initialize_system()
    yield database
    os.remove(test_file_path)
