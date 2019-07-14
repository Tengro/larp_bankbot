import pytest
from bank_bot.banking_system.client_factory import BankingClientFactory
from bank_bot.banking_system.banking_system_class_based import BankingClient
from bank_bot.banking_system.user_class import User
from bank_bot.banking_system import UserError, MessageError
from bank_bot.settings import NO_MESSAGES_FOUND

def test_prepare_message(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash = User.create_user(2, 2, "Test user", database)   
    client = BankingClientFactory(database).create_client(mock_message)
    admin = client.get_user_by_user_hash("0000000000")
    with pytest.raises(UserError):
        client.prepare_message("/message 1234567890 LaLaLaLa")
    with pytest.raises(MessageError):
        client.prepare_message(f"/message {client.user.character_hash} LaLaLaLa")
    chat_id, message = client.prepare_message("/message 0000000000 LaLaLaLa")
    assert message == "LaLaLaLa"
    assert chat_id == admin.chat_id

def test_inspect_messages(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_messages(True) == NO_MESSAGES_FOUND
    assert client.inspect_messages(False) == NO_MESSAGES_FOUND
    chat_id, message  = client.prepare_message(f"/message {character_hash_2} LaLaLaLa")
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_messages(True) != NO_MESSAGES_FOUND
    assert client.inspect_messages(False) == NO_MESSAGES_FOUND
    assert client.inspect_messages(False, character_hash_2) != NO_MESSAGES_FOUND

def test_inspect_all_transactions(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_all_messages() == NO_MESSAGES_FOUND
    assert client.inspect_all_messages(character_hash_2) == NO_MESSAGES_FOUND
    reciever_chat_id, message = client.prepare_message(f"/message {character_hash_2} LaLaLaLa")
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_all_messages() != NO_MESSAGES_FOUND
    assert client.inspect_all_messages(character_hash_2) != NO_MESSAGES_FOUND

def test_inspect_pair_transactions(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_pair_history_messages(f"/messages_history_pair {character_hash_2}") == NO_MESSAGES_FOUND
    assert client.inspect_pair_history_messages(f"/messages_history_pair {character_hash_2}", character_hash_2, character_hash) == NO_MESSAGES_FOUND
    reciever_chat_id, message = client.prepare_message(f"/message {character_hash_2} LaLaLaLa")
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_pair_history_messages(f"/messages_history_pair {character_hash_2}") != NO_MESSAGES_FOUND
    assert client.inspect_pair_history_messages(f"/messages_history_pair {character_hash_2}", character_hash_2, character_hash) != NO_MESSAGES_FOUND
    assert client.inspect_pair_history_messages(f"/messages_history_pair {character_hash_2}") == client.inspect_pair_history_messages(f"/messages_history_pair {character_hash_2}", character_hash_2, character_hash)
