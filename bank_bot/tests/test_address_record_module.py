import pytest
from bank_bot.banking_system.client_factory import BankingClientFactory
from bank_bot.banking_system.banking_system_class_based import BankingClient
from bank_bot.banking_system.user_class import User
from bank_bot.banking_system import AddressRecordError
from bank_bot.settings import NO_ADDRESS_RECORDS, ADDRESS_RECORD_ADDED, ADDRESS_RECORD_DELETION_MESSAGE

def test_add_contact(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(AddressRecordError):
        client.add_contact(f"/add_contact {character_hash} SELF")
    assert client.add_contact(f"/add_contact {character_hash_2} somebody") == ADDRESS_RECORD_ADDED
    with pytest.raises(AddressRecordError):
        client.add_contact(f"/add_contact {character_hash_2} somebody")

def test_delete_contact(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    client.add_contact(f"/add_contact {character_hash_2} somebody")
    assert client.delete_contact(f"/delete_contact {character_hash_2}") == ADDRESS_RECORD_DELETION_MESSAGE

def test_inspect_contact_list(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database) 
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_contact_list() == NO_ADDRESS_RECORDS
    assert client.inspect_contact_list(character_hash_2) == NO_ADDRESS_RECORDS
    client.add_contact(f"/add_contact {character_hash_2} somebody")
    client = BankingClientFactory(database).create_client(mock_message)
    client = BankingClientFactory(database).create_client(mock_message)
    assert client.inspect_contact_list() != NO_ADDRESS_RECORDS
    assert client.inspect_contact_list(character_hash_2) == NO_ADDRESS_RECORDS
