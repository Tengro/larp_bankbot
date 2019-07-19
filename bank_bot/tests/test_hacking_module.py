import pytest
from bank_bot.banking_system.client_factory import BankingClientFactory
from bank_bot.banking_system.banking_system_class_based import BankingClient
from bank_bot.banking_system.user_class import User
from bank_bot.banking_system import UserError, TransactionError, HackerError
from bank_bot.settings import NO_USER_DATA, NO_TRANSACTIONS_FOUND, DEFAULT_FINANCES, ATTRIBUTE_UPDATE_MESSAGE, NO_MESSAGES_FOUND
from bank_bot.banking_system.transaction_class import Transaction
from bank_bot.banking_system.message_class import Message

def test_hacker_validation(database, mock_message):
    character_hash = User.create_user(2, 2, "Test user", database)
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(HackerError):
        client.hacker_validation(0)
    User.update_db_value(character_hash, "hacker_level", 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    with pytest.raises(HackerError):
        client.hacker_validation(2)
    client.hacker_validation(0)

def test_hack_inspect_user(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash, "hacker_level", 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_4 = User.create_user(4, 4, "Test user 4", database)
    User.update_db_value(character_hash_4, "hacker_defence", 1, database)
    user2 = client.get_user_by_user_hash(character_hash_2)
    user4 = client.get_user_by_user_hash(character_hash_4)
    with pytest.raises(UserError):
        client.hack_inspect_user("/hack 1234567890")
    resulting_data, chat_id, show_hack = client.hack_inspect_user(f'/hack {character_hash_2}')
    assert resulting_data == user2.hack_result
    assert chat_id == user2.chat_id
    assert not show_hack
    with pytest.raises(HackerError):
        client.hack_inspect_user(f'/hack 0000000000')
    resulting_data, chat_id, show_hack = client.hack_inspect_user(f'/hack {character_hash_4}')
    assert resulting_data == user4.hack_result
    assert chat_id == user4.chat_id
    assert show_hack

def test_hack_inspect_transactions(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash_1 = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash_1, "hacker_level", 1, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)
    User.update_db_value(character_hash_3, "hacker_defence", 1, database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results, chat_id, show_hack =  client.hack_inspect_transactions(f"/hack_history_sent {character_hash_2}", True)
    assert results == NO_TRANSACTIONS_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_transactions(f"/hack_history_recieved {character_hash_2}", False)
    assert results == NO_TRANSACTIONS_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_transactions(f"/hack_history_recieved {character_hash_3}", False)
    assert results == NO_TRANSACTIONS_FOUND
    assert show_hack

    Transaction.create_transaction(character_hash_2, character_hash_4, 100, database)
    Transaction.create_transaction(character_hash_2, character_hash_3, 100, database)
    Transaction.create_transaction(character_hash_2, "0000000000", 100, database)

    results, chat_id, show_hack =  client.hack_inspect_transactions(f"/hack_history_sent {character_hash_2}", True)
    assert results != NO_TRANSACTIONS_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_transactions(f"/hack_history_recieved {character_hash_2}", False)
    assert results == NO_TRANSACTIONS_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_transactions(f"/hack_history_recieved {character_hash_3}", False)
    assert results != NO_TRANSACTIONS_FOUND
    assert show_hack

    with pytest.raises(HackerError):
        client.hack_inspect_transactions(f"/hack_history_recieved 0000000000", False)

def test_hack_inspect_all_transactions(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash_1 = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash_1, "hacker_level", 1, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)
    User.update_db_value(character_hash_3, "hacker_defence", 1, database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results, chat_id, show_hack =  client.hack_inspect_all_transactions(f"/hack_history_all {character_hash_2}")
    assert results == NO_TRANSACTIONS_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_all_transactions(f"/hack_history_all {character_hash_3}")
    assert results == NO_TRANSACTIONS_FOUND
    assert show_hack

    Transaction.create_transaction(character_hash_2, character_hash_4, 100, database)
    Transaction.create_transaction(character_hash_2, character_hash_3, 100, database)
    Transaction.create_transaction(character_hash_2, "0000000000", 100, database)

    results, chat_id, show_hack =  client.hack_inspect_all_transactions(f"/hack_history_all {character_hash_2}")
    assert results != NO_TRANSACTIONS_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_all_transactions(f"/hack_history_all {character_hash_3}")
    assert results != NO_TRANSACTIONS_FOUND
    assert show_hack

    with pytest.raises(HackerError):
        client.hack_inspect_all_transactions(f"/hack_history_all 0000000000")


def test_hack_inspect_pair_transactions(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash_1 = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash_1, "hacker_level", 1, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)
    User.update_db_value(character_hash_3, "hacker_defence", 1, database)
    User.update_db_value(character_hash_4, "hacker_defence", 2, database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history(f"/hack_history_pair {character_hash_2} {character_hash_3}")
    assert results == NO_TRANSACTIONS_FOUND
    assert not show_hack
    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history(f"/hack_history_pair {character_hash_4} {character_hash_3}")
    assert results == NO_TRANSACTIONS_FOUND
    assert show_hack
    with pytest.raises(HackerError):
        client.hack_inspect_pair_history(f"/hack_history_pair {character_hash_4} 0000000000")

    Transaction.create_transaction(character_hash_2, character_hash_4, 100, database)
    Transaction.create_transaction(character_hash_2, character_hash_3, 100, database)
    Transaction.create_transaction(character_hash_2, "0000000000", 100, database)
    Transaction.create_transaction(character_hash_3, character_hash_4, 100, database)

    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history(f"/hack_history_pair {character_hash_2} {character_hash_3}")
    assert results != NO_TRANSACTIONS_FOUND
    assert not show_hack
    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history(f"/hack_history_pair {character_hash_2} 0000000000")
    assert results != NO_TRANSACTIONS_FOUND
    assert not show_hack
    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history(f"/hack_history_pair {character_hash_4} {character_hash_3}")
    assert results != NO_TRANSACTIONS_FOUND
    assert show_hack

def test_hack_inspect_messages(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash_1 = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash_1, "hacker_level", 1, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)
    User.update_db_value(character_hash_3, "hacker_defence", 1, database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results, chat_id, show_hack =  client.hack_inspect_messages(f"/hack_messages_history_sent {character_hash_2}", True)
    assert results == NO_MESSAGES_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_messages(f"/hack_messages_history_recieved {character_hash_2}", False)
    assert results == NO_MESSAGES_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_messages(f"/hack_messages_history_recieved {character_hash_3}", False)
    assert results == NO_MESSAGES_FOUND
    assert show_hack

    Message.create_message(character_hash_2, character_hash_4, "100", database)
    Message.create_message(character_hash_2, character_hash_3, "100", database)
    Message.create_message(character_hash_2, "0000000000", "100", database)

    results, chat_id, show_hack =  client.hack_inspect_messages(f"/hack_messages_history_sent {character_hash_2}", True)
    assert results != NO_MESSAGES_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_messages(f"/hack_messages_history_recieved {character_hash_2}", False)
    assert results == NO_MESSAGES_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_messages(f"/hack_messages_history_recieved {character_hash_3}", False)
    assert results != NO_MESSAGES_FOUND
    assert show_hack

    with pytest.raises(HackerError):
        client.hack_inspect_messages(f"/hack_messages_history_recieved 0000000000", False)

def test_hack_inspect_all_messages(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash_1 = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash_1, "hacker_level", 1, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)
    User.update_db_value(character_hash_3, "hacker_defence", 1, database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results, chat_id, show_hack =  client.hack_inspect_all_messages(f"/hack_messages_history_all {character_hash_2}")
    assert results == NO_MESSAGES_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_all_messages(f"/hack_messages_history_all {character_hash_3}")
    assert results == NO_MESSAGES_FOUND
    assert show_hack

    Message.create_message(character_hash_2, character_hash_4, "100", database)
    Message.create_message(character_hash_2, character_hash_3, "100", database)
    Message.create_message(character_hash_2, "0000000000", "100", database)

    results, chat_id, show_hack =  client.hack_inspect_all_messages(f"/hack_messages_history_all {character_hash_2}")
    assert results != NO_MESSAGES_FOUND
    assert not show_hack
    results, chat_id, show_hack = client.hack_inspect_all_messages(f"/hack_messages_history_all {character_hash_3}")
    assert results != NO_MESSAGES_FOUND
    assert show_hack

    with pytest.raises(HackerError):
        client.hack_inspect_all_messages(f"/hack_messages_history_all 0000000000")


def test_hack_inspect_pair_messages(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash_1 = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash_1, "hacker_level", 1, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_3 = User.create_user(4, 4, "Test user 3", database)
    character_hash_4 = User.create_user(5, 5, "Test user 4", database)
    User.update_db_value(character_hash_3, "hacker_defence", 1, database)
    User.update_db_value(character_hash_4, "hacker_defence", 2, database)

    client = BankingClientFactory(database).create_client(mock_message)
 
    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history_messages(f"/hack_messages_history_pair {character_hash_2} {character_hash_3}")
    assert results == NO_MESSAGES_FOUND
    assert not show_hack
    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history_messages(f"/hack_messages_history_pair {character_hash_4} {character_hash_3}")
    assert results == NO_MESSAGES_FOUND
    assert show_hack
    with pytest.raises(HackerError):
        client.hack_inspect_pair_history_messages(f"/hack_messages_history_pair {character_hash_4} 0000000000")

    Message.create_message(character_hash_2, character_hash_4, "100", database)
    Message.create_message(character_hash_2, character_hash_3, "100", database)
    Message.create_message(character_hash_2, "0000000000", "100", database)
    Message.create_message(character_hash_3, character_hash_4, "100", database)

    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history_messages(f"/hack_messages_history_pair {character_hash_2} {character_hash_3}")
    assert results != NO_MESSAGES_FOUND
    assert not show_hack
    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history_messages(f"/hack_messages_history_pair {character_hash_2} 0000000000")
    assert results != NO_MESSAGES_FOUND
    assert not show_hack
    results, chat_id, hash_1, chat_2_id, hash_2, show_hack = client.hack_inspect_pair_history_messages(f"/hack_messages_history_pair {character_hash_4} {character_hash_3}")
    assert results != NO_MESSAGES_FOUND
    assert show_hack

def test_hack_send_hacked_message(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash, "hacker_level", 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_4 = User.create_user(4, 4, "Test user 4", database)
    User.update_db_value(character_hash_4, "hacker_defence", 1, database)
    user2 = client.get_user_by_user_hash(character_hash_2)
    user4 = client.get_user_by_user_hash(character_hash_4)
    with pytest.raises(UserError):
        client.prepare_hacker_message("/h@ck_message 1234567890 OLOLO")
    chat_id, sent_message, show_hack = client.prepare_hacker_message(f'/h@ck_message {character_hash_2} OLOLO')
    assert sent_message == "OLOLO"
    assert chat_id == user2.chat_id
    assert not show_hack
    with pytest.raises(HackerError):
        client.hack_inspect_user(f'/h@ck_message 0000000000 OLOLO')
    chat_id, sent_message, show_hack= client.prepare_hacker_message(f'/h@ck_message {character_hash_4} OLOLO')
    assert sent_message == "OLOLO"
    assert chat_id == user4.chat_id
    assert show_hack


def test_create_hacked_transaction(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash, "hacker_level", 1, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_4 = User.create_user(4, 4, "Test user 4", database)
    User.update_db_value(character_hash_4, "hacker_defence", 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    double_amount = DEFAULT_FINANCES * 2
    half_amount = DEFAULT_FINANCES / 2
    user2 = client.get_user_by_user_hash(character_hash_2)
    user1 = client.get_user_by_user_hash(character_hash)
    assert user2.finances == DEFAULT_FINANCES
    assert user1.finances == DEFAULT_FINANCES
    with pytest.raises(TransactionError):
        client.create_hacker_transaction(f"/h@ck_theft {character_hash_2} {double_amount}")
    with pytest.raises(TransactionError):
        client.create_hacker_transaction(f"/h@ck_theft {character_hash} {half_amount}")
    with pytest.raises(TransactionError):
        client.create_hacker_transaction(f"/h@ck_theft {character_hash_2} notanumber")
    with pytest.raises(TransactionError):
        client.create_hacker_transaction(f"/h@ck_theft {character_hash_2} 0")
    with pytest.raises(UserError):
        client.create_hacker_transaction(f"/h@ck_theft 1234567890 {half_amount}")
    with pytest.raises(HackerError):
        client.create_hacker_transaction(f"/h@ck_theft 0000000000 {half_amount}")
    hacker_chat_id, hacker_hash, victim_chat_id, transaction_message, show_hack = client.create_hacker_transaction(f"/h@ck_theft {character_hash_2} {half_amount}")
    user2 = client.get_user_by_user_hash(character_hash_2)
    user1 = client.get_user_by_user_hash(character_hash)
    assert user2.finances == DEFAULT_FINANCES - half_amount
    assert user1.finances == DEFAULT_FINANCES + half_amount
    assert hacker_chat_id == user1.chat_id
    assert victim_chat_id == user2.chat_id
    assert not show_hack

    hacker_chat_id, hacker_hash, victim_chat_id, transaction_message, show_hack = client.create_hacker_transaction(f"/h@ck_theft {character_hash_4} {half_amount}")
    user2 = client.get_user_by_user_hash(character_hash_4)
    user = client.get_user_by_user_hash(character_hash)
    assert hacker_chat_id == user1.chat_id
    assert victim_chat_id == user2.chat_id
    assert user2.finances == DEFAULT_FINANCES - half_amount
    assert user.finances == DEFAULT_FINANCES + half_amount + half_amount
    assert show_hack


def test_create_hacked_transaction_other(database, mock_message):
    User.create_admin(1, 1, database)
    character_hash = User.create_user(2, 2, "Test user", database)
    User.update_db_value(character_hash, "hacker_level", 1, database)
    character_hash_2 = User.create_user(3, 3, "Test user 2", database)
    character_hash_4 = User.create_user(4, 4, "Test user 4", database)
    character_hash_5 = User.create_user(5, 5, "Test user 5", database)
    User.update_db_value(character_hash_4, "hacker_defence", 1, database)
    client = BankingClientFactory(database).create_client(mock_message)
    double_amount = DEFAULT_FINANCES * 2
    half_amount = DEFAULT_FINANCES / 2
    user2 = client.get_user_by_user_hash(character_hash_2)
    user1 = client.get_user_by_user_hash(character_hash)
    assert user2.finances == DEFAULT_FINANCES
    assert user1.finances == DEFAULT_FINANCES
    with pytest.raises(TransactionError):
        client.create_hacker_transaction_other(f"/h@ck_theft_other {character_hash_2} {character_hash_5} {double_amount}")
    with pytest.raises(TransactionError):
        client.create_hacker_transaction_other(f"/h@ck_theft_other {character_hash} {character_hash_5} {half_amount}")
    with pytest.raises(TransactionError):
        client.create_hacker_transaction_other(f"/h@ck_theft_other {character_hash_2} {character_hash_5} notanumber")
    with pytest.raises(TransactionError):
        client.create_hacker_transaction_other(f"/h@ck_theft_other {character_hash_2} {character_hash_5} 0")
    with pytest.raises(UserError):
        client.create_hacker_transaction_other(f"/h@ck_theft_other 1234567890 {character_hash_5} {half_amount}")
    with pytest.raises(HackerError):
        client.create_hacker_transaction_other(f"/h@ck_theft_other 0000000000 {character_hash_5} {half_amount}")
    hacker_hash, victim_chat_id, profiteer_chat_id, transaction_message, show_hack = client.create_hacker_transaction_other(f"/h@ck_theft_other {character_hash_2} {character_hash_5} {half_amount}")
    user2 = client.get_user_by_user_hash(character_hash_2)
    user5 = client.get_user_by_user_hash(character_hash_5)
    assert user2.finances == DEFAULT_FINANCES - half_amount
    assert user5.finances == DEFAULT_FINANCES + half_amount
    assert hacker_hash == client.user.character_hash
    assert victim_chat_id == user2.chat_id
    assert not show_hack

    hacker_hash, victim_chat_id, profiteer_chat_id, transaction_message, show_hack = client.create_hacker_transaction_other(f"/h@ck_theft_other {character_hash_4} {character_hash_5} {half_amount}")
    user4 = client.get_user_by_user_hash(character_hash_4)
    user5 = client.get_user_by_user_hash(character_hash_5)
    assert hacker_hash == client.user.character_hash
    assert victim_chat_id == user4.chat_id
    assert user4.finances == DEFAULT_FINANCES - half_amount
    assert user5.finances == DEFAULT_FINANCES + half_amount + half_amount
    assert show_hack
