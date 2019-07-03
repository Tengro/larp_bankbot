import sqlite3
from bank_bot.banking_system.user_class import User
from bank_bot.settings import DEFAULT_FINANCES

def test_create_admin(database):
    User.create_admin(1, 1, database)
    conn = sqlite3.connect(database.database_file)
    cursor = conn.cursor()
    user_data = cursor.execute(
        """
        SELECT * from users WHERE character_hash=?
        """,
        ("0000000000",)
    )
    user_data = user_data.fetchone()
    conn.close()
    assert user_data is not None

def test_get_user_by_id(database):
    User.create_admin(1, 1, database)
    user_data = User.get_user_by_id(1, database)
    assert user_data is not None
    user_data = User.get_user_by_id(2, database)
    assert user_data is None

def test_get_user_by_name(database):
    User.create_admin(1, 1, database)
    user_data = User.get_user_by_name("ADMIN", database)
    assert user_data is not None
    user_data = User.get_user_by_name("NOT ADMIN", database)
    assert user_data is None

def test_get_user_by_user_hash(database):
    User.create_admin(1, 1, database)
    user_data = User.get_user_by_user_hash("0000000000", database)
    assert user_data is not None
    user_data = User.get_user_by_user_hash("0000000001", database)
    assert user_data is None

def test_get_user_by_user_hash(database):
    User.create_admin(1, 1, database)
    user_data = User.get_user_by_user_hash("0000000000", database)
    assert user_data is not None
    User.delete_by_hash("0000000000", database)
    user_data = User.get_user_by_user_hash("0000000000", database)
    assert user_data is None

def test_create_user(database):
    character_hash = User.create_user(2, 2, "Test user", database)
    user_data = User.get_user_by_user_hash(character_hash, database)
    assert user_data is not None 
    assert user_data.finances == DEFAULT_FINANCES
    user_data = User.get_user_by_user_hash("0000000000", database)
    assert user_data is None

def test_inspect_all_users(database):
    data = User.inspect_all_users(database)
    assert len(data) == 0
    User.create_admin(1, 1, database)
    data = User.inspect_all_users(database)
    assert len(data) == 1
    character_hash = User.create_user(2, 2, "Test user", database)
    data = User.inspect_all_users(database)
    assert len(data) == 2

def test_update_db_value(database):
    character_hash = User.create_user(2, 2, "Test user", database)
    user_data = User.get_user_by_user_hash(character_hash, database)
    assert user_data is not None 
    assert user_data.finances == DEFAULT_FINANCES
    User.update_db_value(character_hash, "finances", DEFAULT_FINANCES + 1, database)
    user_data = User.get_user_by_user_hash(character_hash, database)
    assert user_data is not None 
    assert user_data.finances == DEFAULT_FINANCES + 1
