import sqlite3
from bank_bot.settings import DATABASE_FILE, DATETIME_FORMAT, TRANSACTION_MODEL_DATA

class Transaction(object):
    def __init__(
        self, sender_hash, recepient_hash, amount, transaction_hash, created_time=None
    ):
        self.sender_hash = sender_hash
        self.recepient_hash = recepient_hash
        self.amount = amount
        self.transaction_hash = transaction_hash
        self.created_time = created_time

    def __str__(self):
        return TRANSACTION_MODEL_DATA.substitute(
            sender_hash=self.sender_hash, reciever_hash=self.recepient_hash, 
            amount=self.amount, created=self.created_time, transaction_hash=self.transaction_hash
        )
        

    def create_db_record(self):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO transactions VALUES(?, ?, ?, ?, ?,)
            """,
            (
                self.sender_hash, self.recepient_hash, self.amount, self.transaction_hash, self.created_time,
            )
        )
        conn.commit()
        conn.close()

    def update_db_value(self, field_name, value):
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE transactions SET {field_name} = {value} WHERE transaction_hash=?;
            """,
            (self.transaction_hash,)
        )
        conn.commit()
        conn.close()

    @classmethod
    def list_transactions(cls, user_hash, is_sender):
        conn = sqlite3.connect(DATABASE_FILE)
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
            transactions.append(cls(*transaction))
        return transactions    
