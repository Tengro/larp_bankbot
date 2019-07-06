import sqlite3
from bank_bot.settings import DATABASE_FILE, USER_MODEL_DATA

class User(object):
    def __init__(
        self, user_id, chat_id, character_name, character_hash,
        finances, created, hacker_level, hacker_defence, is_admin
    ):
        self.user_id = user_id
        self.chat_id = chat_id
        self.character_name = character_name
        self.character_hash = character_hash
        self.finances = finances
        self.created = created
        self.hacker_level = hacker_level
        self.hacker_defence = hacker_defence
        self.is_admin = is_admin

    def __str__(self):
        return USER_MODEL_DATA.substitute(
            character_name=self.character_name, character_hash=self.character_hash,
            finances=self.finances, created=self.created, hack_level=self.hacker_level,
            defence_level=self.hacker_defence
        )

    @classmethod
    def get_user_by_id(cls, user_id, database):
        user_data = database.get_user('user_id', user_id)
        if user_data is None:
            return user_data
        else:
            return cls(*user_data)

    @classmethod
    def get_admin_list(cls, database):
        return database.get_admin_list(cls)

    @classmethod
    def get_user_by_name(cls, user_name, database):
        user_data = database.get_user('character_name', user_name)
        if user_data is None:
            return user_data
        else:
            return cls(*user_data)

    @classmethod
    def get_user_by_user_hash(cls, character_hash, database):
        user_data = database.get_user('character_hash', character_hash)
        if user_data is None:
            return user_data
        else:
            return cls(*user_data)

    @classmethod
    def delete_by_hash(cls, target_user_hash, database):
        database.delete_user(target_user_hash)

    @classmethod
    def inspect_all_users(cls, database):
        return database.inspect_all_users(cls)

    @classmethod
    def create_admin(self, user_id, chat_id, database):
        database.create_admin(user_id, chat_id)

    @classmethod
    def create_user(self, user_id, chat_id, character_name, database):
        return database.create_user(user_id, chat_id, character_name)

    @classmethod
    def update_db_value(self, user_hash, field_name, value, database):
        database.update_user_value(user_hash, field_name, value)
