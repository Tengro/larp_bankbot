from bank_bot.banking_system.user_class import User
from bank_bot.banking_system.address_record_class import AddressRecord
from bank_bot.settings import DEFAULT_FINANCES

def test_create_address_record(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    AddressRecord.create_address_record(user_hash_1, user_hash_2, "FIRST", database)

def test_list_address_records(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    assert len(AddressRecord.list_address_records(user_hash_1, database)) == 0
    assert len(AddressRecord.list_address_records(user_hash_2, database)) == 0
    AddressRecord.create_address_record(user_hash_1, user_hash_2, "FIRST", database)
    assert len(AddressRecord.list_address_records(user_hash_1, database)) == 1
    assert len(AddressRecord.list_address_records(user_hash_2, database)) == 0


def test_delete_address_record(database):
    user_hash_1 = User.create_user(2, 2, "Test user 1", database)
    user_hash_2 = User.create_user(3, 3, "Test user 2", database)
    AddressRecord.create_address_record(user_hash_1, user_hash_2, "FIRST", database)
    assert len(AddressRecord.list_address_records(user_hash_1, database)) == 1
    AddressRecord.delete_address_record(user_hash_1, user_hash_2, database)
    assert len(AddressRecord.list_address_records(user_hash_1, database)) == 0
