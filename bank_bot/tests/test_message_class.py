from bank_bot.banking_system.user_class import User
from bank_bot.banking_system.message_class import Message
from bank_bot.settings import DEFAULT_FINANCES

def test_create_messages(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    Message.create_message(user_hash_1, user_hash_2, "HELLO", database)

def test_list_messages_sender(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    assert len(Message.inspect_messages(user_hash_1, True, database)) == 0
    assert len(Message.inspect_messages(user_hash_2, True, database)) == 0
    Message.create_message(user_hash_1, user_hash_2, "HELLO", database)
    assert len(Message.inspect_messages(user_hash_1, True, database)) == 1
    assert len(Message.inspect_messages(user_hash_2, True, database)) == 0


def test_list_messages_reciever(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    assert len(Message.inspect_messages(user_hash_1, False, database)) == 0
    assert len(Message.inspect_messages(user_hash_2, False, database)) == 0
    Message.create_message(user_hash_1, user_hash_2, "HELLO", database)
    assert len(Message.inspect_messages(user_hash_1, False, database)) == 0
    assert len(Message.inspect_messages(user_hash_2, False, database)) == 1

def test_list_messages_all(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    assert len(Message.inspect_all_messages(user_hash_1, database)) == 0
    assert len(Message.inspect_all_messages(user_hash_2, database)) == 0
    Message.create_message(user_hash_1, user_hash_2, "HELLO", database)
    assert len(Message.inspect_all_messages(user_hash_1, database)) == 1
    assert len(Message.inspect_all_messages(user_hash_2, database)) == 1

def test_list_messages_pair(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    assert len(Message.inspect_pair_history_messages(user_hash_1, user_hash_2, database)) == 0
    assert len(Message.inspect_pair_history_messages(user_hash_2, user_hash_1, database)) == 0
    Message.create_message(user_hash_1, user_hash_2, "HELLO", database)
    assert len(Message.inspect_pair_history_messages(user_hash_1, user_hash_2, database)) == len(Message.inspect_pair_history_messages(user_hash_2, user_hash_1, database))
