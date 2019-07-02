import sqlite3
from bank_bot.settings import DATABASE_FILE

def initialize_system():
    conn = sqlite3.connect(DATABASE_FILE)
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

