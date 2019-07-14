from bank_bot.banking_system.user_class import User
from bank_bot.banking_system.transaction_class import Transaction
from bank_bot.settings import DEFAULT_FINANCES

def test_create_transactions(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    Transaction.create_transaction(user_hash_1, user_hash_2, 100, database)

def test_list_transactions_sender(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    assert len(Transaction.list_transactions(user_hash_1, True, database)) == 0
    assert len(Transaction.list_transactions(user_hash_2, True, database)) == 0
    Transaction.create_transaction(user_hash_1, user_hash_2, 100, database)
    assert len(Transaction.list_transactions(user_hash_1, True, database)) == 1
    assert len(Transaction.list_transactions(user_hash_2, True, database)) == 0


def test_list_transactions_reciever(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    assert len(Transaction.list_transactions(user_hash_1, False, database)) == 0
    assert len(Transaction.list_transactions(user_hash_2, False, database)) == 0
    Transaction.create_transaction(user_hash_1, user_hash_2, 100, database)
    assert len(Transaction.list_transactions(user_hash_1, False, database)) == 0
    assert len(Transaction.list_transactions(user_hash_2, False, database)) == 1

