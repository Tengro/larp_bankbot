import sqlite3
from bank_bot.settings import DATABASE_FILE, USER_MODEL_DATA

class User(object):
    def __init__(
        self, user_id, chat_id, character_name, character_hash,
        finances, created_time, hacker_level, hacker_defence, is_admin
    ):
        self.user_id = user_id
        self.chat_id = chat_id
        self.character_name = character_name
        self.character_hash = character_hash
        self.finances = finances
        self.created_time = created_time
        self.hacker_level = hacker_level
        self.hacker_defence = hacker_defence
        self.is_admin = is_admin

    def __str__(self):
        return USER_MODEL_DATA.substitute(
            character_name=self.character_name, character_hash=self.character_hash,
            finances=self.finances, created=self.created_time, hack_level=self.hacker_level,
            defence_level=self.hacker_defence
        )

    @classmethod
    def get_user_by_id(cls, user_id):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        user_data = cursor.execute(
            """
            SELECT * from users WHERE user_id=?
            """,
            (user_id,)
        )
        user_data = user_data.fetchone()
        conn.close()
        if not user_data:
            return None
        return cls(*user_data)

    @classmethod
    def get_user_by_user_hash(cls, character_hash):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        user_data = cursor.execute(
            """
            SELECT * from users WHERE character_hash=?
            """,
            (character_hash,)
        )
        user_data = user_data.fetchone()
        conn.close()
        if not user_data:
            return None
        return User(*user_data)

    @classmethod
    def delete_by_hash(cls, target_user_hash):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM users WHERE user_hash=?
            """,
            (target_user_hash,)
        )
        conn.commit()
        conn.close()

    @classmethod
    def inspect_all_users(cls):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        user_data = cursor.execute(
            """
            SELECT * from users ORDER BY created
            """,
        )
        all_user_data = user_data.fetchall()
        conn.close()
        all_users = []
        for user_data in all_user_data:
            all_users.append(cls(*user_data))
        return all_users

    def create_db_record(self):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.user_id, self.chat_id, self.character_name, self.character_hash, self.finances,
                self.created_time, self.hacker_level, self.hacker_defence, self.is_admin
            )
        )
        conn.commit()
        conn.close()

    def update_db_value(self, field_name, value):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE users SET {field_name} = {value} WHERE character_hash=?;
            """,
            (self.character_hash,)
        )
        conn.commit()
        conn.close()
