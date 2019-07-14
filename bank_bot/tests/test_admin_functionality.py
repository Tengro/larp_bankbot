import pytest
from bank_bot.banking_system.client_factory import BankingClientFactory
from bank_bot.banking_system.banking_system_class_based import BankingClient
from bank_bot.banking_system.user_class import User
from bank_bot.banking_system import UserError, AddressRecordError
from bank_bot.settings import (
    NO_USER_DATA, NO_TRANSACTIONS_FOUND, DEFAULT_FINANCES, ATTRIBUTE_UPDATE_MESSAGE,
    NO_MESSAGES_FOUND, NO_ADDRESS_RECORDS, ADDRESS_RECORD_ADDED, ADDRESS_RECORD_DELETION_MESSAGE
)
from bank_bot.banking_system.transaction_class import Transaction
from bank_bot.banking_system.message_class import Message

def test_admin_validation(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    User.create_admin(1, 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.admin_validation()
    mock_message.json['from']['id'] = 1
    client = BankingClientFactory(database).create_client(mock_message)
    client.admin_validation()

def test_create_admin(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(UserError):
        client.create_admin()
    mock_message.json['from']['id'] = 1
    client = BankingClientFactory(database).create_client(mock_message)
    client.create_admin() 

def test_delete_user(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash = User.create_user(3, 3, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.get_user_by_user_hash(character_hash) is not None
    client.delete_user(f"/delete {character_hash}")
    with pytest.raises(UserError):
        client.get_user_by_user_hash(character_hash)

def test_inspect_all_users(database, mock_message):
    User.create_admin(2, 2, database)
    client = BankingClientFactory(database).create_client(mock_message)
    user = client.get_user_by_user_hash("0000000000")
    assert client.inspect_all_users() == str(user) + '\n\n'

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

def test_get_admins(database, mock_message):
    User.create_admin(2, 2, database)
    client = BankingClientFactory(database).create_client(mock_message)
    admin_list = client.get_admins()
    assert len(admin_list) == 1

def test_admin_hail_users(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash = User.create_user(4, 4, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    message_list = client.admin_hail_users("/hail_users TEST MESSAGE")
    assert len(message_list) == 2
    assert 2 not in [x.chat_id for x in message_list]
    assert message_list[0].message == "TEST MESSAGE"

def test_admin_inspect_user(database, mock_message):
    User.create_admin(2, 2, database)
    client = BankingClientFactory(database).create_client(mock_message)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    user2 = client.get_user_by_user_hash(character_hash_2)
    with pytest.raises(UserError):
        client.admin_inspect_user("/admin_inspect_user 1234567890")
    resulting_data = client.admin_inspect_user(f'/admin_inspect_user {character_hash_2}')
    assert resulting_data == str(user2)

def test_admin_inspect_transactions(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results =  client.admin_inspect_transactions(f"/admin_history_sent {character_hash_2}", True)
    assert results == NO_TRANSACTIONS_FOUND
    results = client.admin_inspect_transactions(f"/admin_history_recieved {character_hash_2}", False)
    assert results == NO_TRANSACTIONS_FOUND
    results = client.admin_inspect_transactions(f"/admin_history_recieved {character_hash_3}", False)
    assert results == NO_TRANSACTIONS_FOUND

    Transaction.create_transaction(character_hash_2, character_hash_3, 100, database)
    Transaction.create_transaction(character_hash_2, "0000000000", 100, database)

    results =  client.admin_inspect_transactions(f"/admin_history_sent {character_hash_2}", True)
    assert results != NO_TRANSACTIONS_FOUND
    results = client.admin_inspect_transactions(f"/admin_history_recieved {character_hash_2}", False)
    assert results == NO_TRANSACTIONS_FOUND
    results = client.admin_inspect_transactions(f"/admin_history_recieved {character_hash_3}", False)
    assert results != NO_TRANSACTIONS_FOUND


def test_admin_inspect_all_transactions(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results =  client.admin_inspect_all_transactions(f"/admin_history_all {character_hash_2}")
    assert results == NO_TRANSACTIONS_FOUND
    results = client.admin_inspect_all_transactions(f"/admin_history_all {character_hash_3}")
    assert results == NO_TRANSACTIONS_FOUND

    Transaction.create_transaction(character_hash_2, character_hash_4, 100, database)
    Transaction.create_transaction(character_hash_2, character_hash_3, 100, database)
    Transaction.create_transaction(character_hash_2, "0000000000", 100, database)

    results =  client.admin_inspect_all_transactions(f"/admin_history_all {character_hash_2}")
    assert results != NO_TRANSACTIONS_FOUND
    results = client.admin_inspect_all_transactions(f"/admin_history_all {character_hash_3}")
    assert results != NO_TRANSACTIONS_FOUND


def test_admin_inspect_pair_transactions(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results = client.admin_inspect_pair_history(f"/admin_history_pair {character_hash_2} {character_hash_3}")
    assert results == NO_TRANSACTIONS_FOUND
    results = client.admin_inspect_pair_history(f"/admin_history_pair {character_hash_4} {character_hash_3}")
    assert results == NO_TRANSACTIONS_FOUND

    Transaction.create_transaction(character_hash_2, character_hash_4, 100, database)
    Transaction.create_transaction(character_hash_2, character_hash_3, 100, database)
    Transaction.create_transaction(character_hash_2, "0000000000", 100, database)
    Transaction.create_transaction(character_hash_3, character_hash_4, 100, database)

    results = client.admin_inspect_pair_history(f"/admin_history_pair {character_hash_2} {character_hash_3}")
    assert results != NO_TRANSACTIONS_FOUND
    results = client.admin_inspect_pair_history(f"/admin_history_pair {character_hash_4} {character_hash_3}")
    assert results != NO_TRANSACTIONS_FOUND

def test_admin_inspect_messages(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results =  client.admin_inspect_messages(f"/admin_messages_history_sent {character_hash_2}", True)
    assert results == NO_MESSAGES_FOUND
    results = client.admin_inspect_messages(f"/admin_messages_history_recieved {character_hash_2}", False)
    assert results == NO_MESSAGES_FOUND
    results = client.admin_inspect_messages(f"/admin_messages_history_recieved {character_hash_3}", False)
    assert results == NO_MESSAGES_FOUND

    Message.create_message(character_hash_2, character_hash_3, "100", database)
    Message.create_message(character_hash_2, "0000000000", "100", database)

    results =  client.admin_inspect_messages(f"/admin_messages_history_sent {character_hash_2}", True)
    assert results != NO_MESSAGES_FOUND
    results = client.admin_inspect_messages(f"/admin_messages_history_recieved {character_hash_2}", False)
    assert results == NO_MESSAGES_FOUND
    results = client.admin_inspect_messages(f"/admin_messages_history_recieved {character_hash_3}", False)
    assert results != NO_MESSAGES_FOUND


def test_admin_inspect_all_messages(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results =  client.admin_inspect_all_messages(f"/admin_messages_history_all {character_hash_2}")
    assert results == NO_MESSAGES_FOUND
    results = client.admin_inspect_all_messages(f"/admin_messages_history_all {character_hash_3}")
    assert results == NO_MESSAGES_FOUND

    Message.create_message(character_hash_2, character_hash_4, "100", database)
    Message.create_message(character_hash_2, character_hash_3, "100", database)
    Message.create_message(character_hash_2, "0000000000", "100", database)

    results =  client.admin_inspect_all_messages(f"/admin_messages_history_all {character_hash_2}")
    assert results != NO_MESSAGES_FOUND
    results = client.admin_inspect_all_messages(f"/admin_messages_history_all {character_hash_3}")
    assert results != NO_MESSAGES_FOUND


def test_admin_inspect_pair_messages(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results = client.admin_inspect_pair_history_messages(f"/admin_messages_history_pair {character_hash_2} {character_hash_3}")
    assert results == NO_MESSAGES_FOUND
    results = client.admin_inspect_pair_history_messages(f"/admin_messages_history_pair {character_hash_4} {character_hash_3}")
    assert results == NO_MESSAGES_FOUND

    Message.create_message(character_hash_2, character_hash_4, "100", database)
    Message.create_message(character_hash_2, character_hash_3, "100", database)
    Message.create_message(character_hash_2, "0000000000", "100", database)
    Message.create_message(character_hash_3, character_hash_4, "100", database)

    results = client.admin_inspect_pair_history_messages(f"/admin_messages_history_pair {character_hash_2} {character_hash_3}")
    assert results != NO_MESSAGES_FOUND
    results = client.admin_inspect_pair_history_messages(f"/admin_messages_history_pair {character_hash_4} {character_hash_3}")
    assert results != NO_MESSAGES_FOUND

def test_admin_add_contact(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash = User.create_user(4, 4, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(AddressRecordError):
        client.admin_add_contact(f"/admin_add_contact {character_hash} {character_hash} SELF")
    assert client.admin_add_contact(f"/admin_add_contact {character_hash} {character_hash_2} somebody") == ADDRESS_RECORD_ADDED
    with pytest.raises(AddressRecordError):
        client.admin_add_contact(f"/admin_add_contact {character_hash} {character_hash_2} somebody")

def test_admin_delete_contact(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash = User.create_user(4, 4, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    client.admin_add_contact(f"/admin_add_contact {character_hash} {character_hash_2} somebody")
    assert client.admin_delete_contact(f"/admin_delete_contact {character_hash}  {character_hash_2}") == ADDRESS_RECORD_DELETION_MESSAGE

def test_admin_inspect_contact_list(database, mock_message):
    User.create_admin(2, 2, database)
    character_hash = User.create_user(4, 4, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.admin_inspect_contact_list(f"/admin_inspect_contact_list {character_hash}") == NO_ADDRESS_RECORDS
    assert client.admin_inspect_contact_list(f"/admin_inspect_contact_list {character_hash_2}") == NO_ADDRESS_RECORDS
    client.admin_add_contact(f"/admin_add_contact {character_hash} {character_hash_2} somebody")
    assert client.admin_inspect_contact_list(f"/admin_inspect_contact_list {character_hash}") != NO_ADDRESS_RECORDS
    assert client.admin_inspect_contact_list(f"/admin_inspect_contact_list {character_hash_2}") == NO_ADDRESS_RECORDS