import sqlite3
from datetime import datetime
from hashlib import sha256
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
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                sender_hash text, recepient_hash text, message_text text,
                created_time text
            );
            """
        )
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS address_records (
                owner_hash text, target_hash text, target_name text
            );
            """
        )
        conn.close()

    def get_user(self, search_term, value):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        user_data = cursor.execute(
            """
            SELECT * from users WHERE {search_term}=? COLLATE NOCASE
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
        character_hash = str(abs(int(sha256(character_name.encode('utf-8')).hexdigest(), 16)))[:10]
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

    def get_admin_list(self, klass):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        user_data = cursor.execute(
            """
            SELECT * from users WHERE is_admin=1 ORDER BY created 
            """,
        )
        all_user_data = user_data.fetchall()
        conn.close()
        all_users = []
        for user_data in all_user_data:
            all_users.append(klass(*user_data))
        return all_users

    def create_transaction(self, sender_hash, recepient_hash, amount):
        transaction_hash = str(abs(int(sha256((sender_hash + recepient_hash).encode('utf-8')).hexdigest(), 16)))[:15]
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
        return transaction_hash

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

    def inspect_all_transactions(self, user_hash, klass):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        transaction_data = cursor.execute(
            """
            SELECT * from transactions WHERE sender_hash=? OR recepient_hash=? ORDER BY created_time
            """,
            (user_hash,user_hash)
        )
        transaction_data = transaction_data.fetchall()
        conn.close()
        transactions = []
        for transaction in transaction_data:
            transactions.append(klass(*transaction))
        return transactions    

    def inspect_pair_history_transactions(self, sender_hash, recepient_hash, klass):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        transaction_data = cursor.execute(
            """
            SELECT * from transactions WHERE sender_hash IN (?,?) AND recepient_hash IN (?,?) ORDER BY created_time
            """,
            (sender_hash, recepient_hash, sender_hash, recepient_hash)
        )
        transaction_data = transaction_data.fetchall()
        conn.close()
        transactions = []
        for transaction in transaction_data:
            transactions.append(klass(*transaction))
        return transactions

    def create_message(self, sender_hash, recepient_hash, message_text):
        created = datetime.now().strftime(DATETIME_FORMAT)
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO messages VALUES(?, ?, ?, ?)
            """,
            (
                sender_hash, recepient_hash, message_text, created,
            )
        )
        conn.commit()
        conn.close()

    def inspect_messages(self, user_hash, is_sender, klass):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        search_term = 'sender_hash' if is_sender else 'recepient_hash'
        messages_data = cursor.execute(
            """
            SELECT * from messages WHERE {}=? ORDER BY created_time
            """.format(search_term),
            (user_hash,)
        )
        messages_data = messages_data.fetchall()
        conn.close()
        messages = []
        for message in messages_data:
            messages.append(klass(*message))
        return messages    

    def inspect_all_messages(self, user_hash, klass):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        messages_data = cursor.execute(
            """
            SELECT * from messages WHERE sender_hash=? OR recepient_hash=? ORDER BY created_time
            """,
            (user_hash,user_hash)
        )
        messages_data = messages_data.fetchall()
        conn.close()
        messages = []
        for message in messages_data:
            messages.append(klass(*message))
        return messages   

    def inspect_pair_history_messages(self, sender_hash, recepient_hash, klass):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        messages_data = cursor.execute(
            """
            SELECT * from messages WHERE sender_hash IN (?,?) AND recepient_hash IN (?,?) ORDER BY created_time
            """,
            (sender_hash, recepient_hash, sender_hash, recepient_hash)
        )
        messages_data = messages_data.fetchall()
        conn.close()
        messages = []
        for message in messages_data:
            messages.append(klass(*message))
        return messages

    def create_address_record(self, owner_hash, target_hash, target_name):
        created = datetime.now().strftime(DATETIME_FORMAT)
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO address_records VALUES(?, ?, ?)
            """,
            (
                owner_hash, target_hash, target_name,
            )
        )
        conn.commit()
        conn.close()

    def inspect_address_records(self, owner_hash, klass):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        address_records_data = cursor.execute(
            """
            SELECT * from address_records WHERE owner_hash=?
            """,
            (owner_hash,)
        )
        address_records_data = address_records_data.fetchall()
        conn.close()
        address_records = []
        for address_record in address_records_data:
            address_records.append(klass(*address_record))
        return address_records    

    def delete_address_record(self, owner_hash, target_hash):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM address_records WHERE owner_hash=? AND target_hash=?
            """,
            (owner_hash, target_hash,)
        )
        conn.commit()
        conn.close()
