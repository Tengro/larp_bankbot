import sqlite3
from datetime import datetime
from hashlib import md5
from bank_bot.settings import DEFAULT_FINANCES, DATETIME_FORMAT

class Database(object):
    def __init__(self, file_path):
        self.database_file = file_path

    def initialize_system(self):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id text, chat_id text, character_name text, character_hash text,
                finances real, created text,
                hacker_level integer,
                hacker_defence integer,
                is_admin integer
            );
        """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                sender_hash text, recepient_hash text, amount real, 
                transaction_hash text, created_time text
            );
            """
        )
        conn.close()

    def get_user(self, search_term, value):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        user_data = cursor.execute(
            """
            SELECT * from users WHERE {search_term}=?
            """.format(search_term=search_term),
            (value,)
        )
        user_data = user_data.fetchone()
        conn.close()
        return user_data

    def delete_user(self, target_user_hash):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM users WHERE character_hash=?
            """,
            (target_user_hash,)
        )
        conn.commit()
        conn.close()

    def create_admin(self, user_id, chat_id):
        created = datetime.now().strftime(DATETIME_FORMAT)

        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, chat_id, "ADMIN", "0000000000", 1000000000,
                created, 999, 999, 1
            )
        )
        conn.commit()
        conn.close()

    def create_user(self, user_id, chat_id, character_name):
        character_hash = str(md5(character_name.encode()).hexdigest()[:10])
        created = datetime.now().strftime(DATETIME_FORMAT)

        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, chat_id, character_name, character_hash, DEFAULT_FINANCES,
                created, 0, 0, 0
            )
        )
        user_data = cursor.execute(
            """
            SELECT * from users WHERE {search_term}=?
            """.format(search_term="character_hash"),
            (character_hash,)
        )
        user_data = user_data.fetchone()
        conn.commit()
        conn.close()

        return character_hash

    def update_user_value(self, user_hash, field_name, value):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE users SET {field_name} = {value} WHERE character_hash=?;
            """,
            (user_hash,)
        )
        conn.commit()
        conn.close()

    def inspect_all_users(self, klass):
        conn = sqlite3.connect(self.database_file)
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
            all_users.append(klass(*user_data))
        return all_users

    def create_transaction(self, sender_hash, recepient_hash, amount):
        transaction_hash = md5((sender_hash + recepient_hash).encode()).hexdigest()[:15]
        created = datetime.now().strftime(DATETIME_FORMAT)
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions VALUES(?, ?, ?, ?, ?)
            """,
            (
                sender_hash, recepient_hash, amount, transaction_hash, created,
            )
        )
        conn.commit()
        conn.close()

    def inspect_transactions(self, user_hash, is_sender, klass):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        search_term = 'sender_hash' if is_sender else 'recepient_hash'
        transaction_data = cursor.execute(
            """
            SELECT * from transactions WHERE {}=? ORDER BY created_time
            """.format(search_term),
            (user_hash,)
        )
        transaction_data = transaction_data.fetchall()
        conn.close()
        transactions = []
        for transaction in transaction_data:
            transactions.append(klass(*transaction))
        return transactions    
