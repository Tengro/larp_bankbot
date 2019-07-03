import sqlite3
import pytest
from bank_bot.banking_system.client_factory import BankingClientFactory
from bank_bot.banking_system.banking_system_class_based import BankingClient
from bank_bot.banking_system.user_class import User
from bank_bot.banking_system import UserError, TransactionError
from bank_bot.settings import NO_USER_DATA, NO_TRANSACTIONS_FOUND, DEFAULT_FINANCES, ATTRIBUTE_UPDATE_MESSAGE



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
    assert client.get_user_by_user_hash("0000000000") is None
    assert client.get_user_by_user_hash(character_hash) is not None

def test_admin_validation(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    User.create_admin(1, 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.admin_validation()
    mock_message.json['from']['id'] = 1
    client = BankingClientFactory(database).create_client(mock_message)
    client.admin_validation()

def test_user_validation(database, mock_message):
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.user_validation()
    character_hash = User.create_user(2, 2, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    client.user_validation()

def test_hacker_validation(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.hacker_validation()
    User.update_db_value(character_hash, "hacker_level", 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    client.hacker_validation()

def test_create_admin(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.create_admin()
    mock_message.json['from']['id'] = 1
    client = BankingClientFactory(database).create_client(mock_message)
    client.create_admin()

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

def test_delete_user(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash = User.create_user(3, 3, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.get_user_by_user_hash(character_hash) is not None
    client.delete_user(f"/delete {character_hash}")
    assert client.get_user_by_user_hash(character_hash) is None

def test_inspect_all_users(database, mock_message):
    User.create_admin(2, 2, database)
    client = BankingClientFactory(database).create_client(mock_message)
    user = client.get_user_by_user_hash("0000000000")
    assert client.inspect_all_users() == str(user) + '\n'

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
    assert client.inspect_user("1234567890") == NO_USER_DATA

def test_hack_inspect_user(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash, "hacker_level", 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    user2 = client.get_user_by_user_hash(character_hash_2)
    admin = client.get_user_by_user_hash("0000000000")
    with pytest.raises(UserError):
        client.hack_inspect_user("/hack 1234567890")
    resulting_data, chat_id, show_hack = client.hack_inspect_user(f'/hack {character_hash_2}')
    assert resulting_data == str(user2)
    assert chat_id == user2.chat_id
    assert not show_hack
    resulting_data, chat_id, show_hack = client.hack_inspect_user(f'/hack 0000000000')
    assert resulting_data == str(admin)
    assert chat_id == admin.chat_id
    assert show_hack

def test_prepare_hack_message(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash, "hacker_level", 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    user2 = client.get_user_by_user_hash(character_hash_2)
    admin = client.get_user_by_user_hash("0000000000")
    with pytest.raises(UserError):
        client.prepare_hacker_message("/hackmessage 1234567890 LaLaLaLa")
    chat_id, message, show_hack = client.prepare_hacker_message(f'/hackmessage {character_hash_2} LaLaLaLa')
    assert message == "LaLaLaLa"
    assert chat_id == user2.chat_id
    assert not show_hack
    chat_id, message, show_hack = client.prepare_hacker_message(f'/hackmessage 0000000000 LaLaLaLa')
    assert message == "LaLaLaLa"
    assert chat_id == admin.chat_id
    assert show_hack 

def test_prepare_message(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash = User.create_user(2, 2, "Test user", database)   
    client = BankingClientFactory(database).create_client(mock_message)
    admin = client.get_user_by_user_hash("0000000000")
    with pytest.raises(UserError):
        client.prepare_message("/message 1234567890 LaLaLaLa")
    chat_id, message = client.prepare_message("/message 0000000000 LaLaLaLa")
    assert message == "LaLaLaLa"
    assert chat_id == admin.chat_id

def test_set_attribute(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash = User.create_user(3, 3, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    user = client.get_user_by_user_hash(character_hash)
    assert user.finances == DEFAULT_FINANCES
    with pytest.raises(UserError):
        client.set_attribute("/set_attribute 1234567890 finances 0")
    assert client.set_attribute(f"/set_attribute {character_hash} finances 0") == ATTRIBUTE_UPDATE_MESSAGE
    user = client.get_user_by_user_hash(character_hash)
    assert user.finances == 0

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
