import pytest
from bank_bot.banking_system.client_factory import BankingClientFactory
from bank_bot.banking_system.banking_system_class_based import BankingClient
from bank_bot.banking_system.user_class import User
from bank_bot.banking_system import UserError, TransactionError, HackerError
from bank_bot.settings import NO_USER_DATA, NO_TRANSACTIONS_FOUND, DEFAULT_FINANCES, ATTRIBUTE_UPDATE_MESSAGE
from bank_bot.banking_system.transaction_class import Transaction


def test_client_creation(database, mock_message):
    client = BankingClientFactory(database).create_client(mock_message)
    assert isinstance(client, BankingClient)
    assert client.user_id == "2"
    assert client.chat_id == "2"
    assert client.user is None

def test_get_user_by_id(database, mock_message):
    client = BankingClientFactory(database).create_client(mock_message)
    character_hash = User.create_user(2, 2, "Test user", database)
    assert client.get_user_by_id("2") is not None
    assert client.get_user_by_id("1") is None

def test_get_user_by_name(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.get_user_by_name("Mock") is None
    assert client.get_user_by_name("Test user") is not None

def test_get_user_by_user_hash(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.get_user_by_user_hash("0000000000")
    assert client.get_user_by_user_hash(character_hash) is not None

def test_user_validation(database, mock_message):
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.user_validation()
    character_hash = User.create_user(2, 2, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    client.user_validation()

def test_register_user(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.register_user("/register Peter Parker")
    mock_message.json['from']['id'] = 1
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.register_user("/register")
    client.register_user("/register Peter Parker")
    mock_message.json['from']['id'] = 3
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.register_user("/register Peter Parker")    

def test_inspect_self(database, mock_message):
    User.create_admin(2, 2, database)
    client = BankingClientFactory(database).create_client(mock_message)
    user = client.get_user_by_user_hash("0000000000")
    assert client.inspect_self() == str(user)

def test_inspect_user(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash = User.create_user(3, 3, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    user = client.get_user_by_user_hash("0000000000")
    user2 = client.get_user_by_user_hash(character_hash)
    assert client.inspect_user() == str(user)
    assert client.inspect_user(character_hash) == str(user2)
    with pytest.raises(UserError):
        client.inspect_user("1234567890")

def test_create_transaction(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    double_amount = DEFAULT_FINANCES * 2
    half_amount = DEFAULT_FINANCES / 2
    user2 = client.get_user_by_user_hash(character_hash_2)
    user1 = client.get_user_by_user_hash(character_hash)
    assert user2.finances == DEFAULT_FINANCES
    assert user1.finances == DEFAULT_FINANCES
    with pytest.raises(TransactionError):
        client.create_transaction(f"/send {character_hash_2} {double_amount}")
    with pytest.raises(TransactionError):
        client.create_transaction(f"/send {character_hash} {half_amount}")
    with pytest.raises(TransactionError):
        client.create_transaction(f"/send {character_hash_2} notanumber")
    with pytest.raises(TransactionError):
        client.create_transaction(f"/send {character_hash_2} 0")
    with pytest.raises(UserError):
        client.create_transaction(f"/send 1234567890 {half_amount}")
    sender_chat_id, reciever_chat_id, message = client.create_transaction(f"/send {character_hash_2} {half_amount}")
    user2 = client.get_user_by_user_hash(character_hash_2)
    user1 = client.get_user_by_user_hash(character_hash)
    assert user2.finances == DEFAULT_FINANCES + half_amount
    assert user1.finances == DEFAULT_FINANCES - half_amount
    assert sender_chat_id == user1.chat_id
    assert reciever_chat_id == user2.chat_id

def test_inspect_transactions(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_transactions(True) == NO_TRANSACTIONS_FOUND
    assert client.inspect_transactions(False) == NO_TRANSACTIONS_FOUND
    half_amount = DEFAULT_FINANCES / 2
    sender_chat_id, reciever_chat_id, message = client.create_transaction(f"/send {character_hash_2} {half_amount}")
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_transactions(True) != NO_TRANSACTIONS_FOUND
    assert client.inspect_transactions(False) == NO_TRANSACTIONS_FOUND
    assert client.inspect_transactions(False, character_hash_2) != NO_TRANSACTIONS_FOUND

def test_inspect_all_transactions(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_all_transactions() == NO_TRANSACTIONS_FOUND
    assert client.inspect_all_transactions(character_hash_2) == NO_TRANSACTIONS_FOUND
    half_amount = DEFAULT_FINANCES / 2
    sender_chat_id, reciever_chat_id, message = client.create_transaction(f"/send {character_hash_2} {half_amount}")
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_all_transactions() != NO_TRANSACTIONS_FOUND
    assert client.inspect_all_transactions(character_hash_2) != NO_TRANSACTIONS_FOUND

def test_inspect_pair_transactions(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_pair_history(f"/history_pair {character_hash_2}") == NO_TRANSACTIONS_FOUND
    assert client.inspect_pair_history(f"/history_pair {character_hash_2}", character_hash_2, character_hash) == NO_TRANSACTIONS_FOUND
    half_amount = DEFAULT_FINANCES / 2
    sender_chat_id, reciever_chat_id, message = client.create_transaction(f"/send {character_hash_2} {half_amount}")
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_pair_history(f"/history_pair {character_hash_2}") != NO_TRANSACTIONS_FOUND
    assert client.inspect_pair_history(f"/history_pair {character_hash_2}", character_hash_2, character_hash) != NO_TRANSACTIONS_FOUND
    assert client.inspect_pair_history(f"/history_pair {character_hash_2}") == client.inspect_pair_history(f"/history_pair {character_hash_2}", character_hash_2, character_hash)
