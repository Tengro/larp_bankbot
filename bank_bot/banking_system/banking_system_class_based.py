import re

from bank_bot.settings import (
    DATETIME_FORMAT, NO_USER_ERROR, NO_ADMIN_ERROR, ALREADY_ADMIN,
    ADMIN_RECORD_CREATED, ALREADY_REGISTERED, NO_NAME, REGISTRATION_MESSAGE,
    DELETION_MESSAGE, TRANSACTION_NO_FINANCES, TRANSACTION_NO_USER, TRANSACTION_MESSAGE,
    NO_HACKER, NO_TRANSACTIONS_FOUND, NO_USER_DATA, ATTRIBUTE_UPDATE_MESSAGE,
    ALREADY_HAVE_USER,ZERO_TRANSACTION, SELF_TRANSACTION, TRANSACTION_UNALLOWED_VALUE
)

from bank_bot.banking_system.user_class import User
from bank_bot.banking_system.transaction_class import Transaction
from bank_bot.banking_system.exceptions import TransactionError, UserError

class BankingClient(object):
    def __init__(self, message, database):
        self.user_id = str(message.json['from']['id'])
        self.chat_id = str(message.json['chat']['id'])
        self.database = database
        self.user = self.get_user_by_id(self.user_id)

    def get_user_by_id(self, user_id):
        user = User.get_user_by_id(user_id, self.database)
        return user

    def get_user_by_name(self, user_name):
        user = User.get_user_by_name(user_name, self.database)
        return user


    def get_user_by_user_hash(self, character_hash):
        user = User.get_user_by_user_hash(character_hash, self.database)
        return user

    def admin_validation(self):
        self.user_validation()
        if not self.user.is_admin:
            raise UserError(NO_ADMIN_ERROR)

    def user_validation(self):
        if self.user is None:
            raise UserError(NO_USER_ERROR)

    def hacker_validation(self):
        self.user_validation()
        if self.user.hacker_level <= 0:
            raise UserError(NO_HACKER)

    def create_admin(self):
        if self.user is not None:
            raise UserError(ALREADY_ADMIN)
        user = User.create_admin(self.user_id, self.chat_id, self.database)
        return ADMIN_RECORD_CREATED

    def register_user(self, message_text):
        if self.user is not None:
            raise UserError(ALREADY_REGISTERED)
        character_name = message_text.strip('/register ')
        character_name = character_name.strip(' ')
        if not character_name:
            raise UserError(NO_NAME)
        user = self.get_user_by_name(character_name)
        if user is not None:
            raise UserError(ALREADY_HAVE_USER)
        character_hash = User.create_user(self.user_id, self.chat_id, character_name, self.database)
        return REGISTRATION_MESSAGE.substitute(character_name=character_name, character_hash=character_hash)

    def delete_user(self, message_text):
        self.admin_validation()
        target_user_hash = message_text.strip('/delete ')
        user = User.delete_by_hash(target_user_hash, self.database)
        return DELETION_MESSAGE.substitute(character_hash=target_user_hash)
        
    def inspect_all_users(self):
        self.admin_validation()
        all_users = User.inspect_all_users(self.database)
        resulting_data = ""
        for user in all_users:
            resulting_data += str(user) + '\n\n'
        return resulting_data

    def inspect_self(self):
        return self.inspect_user()

    def inspect_user(self, user_hash=None):
        self.user_validation()
        if user_hash is None:
            user_hash = self.user.character_hash
        user = self.get_user_by_user_hash(user_hash)
        if not user:
            return NO_USER_DATA
        return str(user)

    def hack_inspect_user(self, message):
        self.hacker_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        if not target_user:
            raise UserError(NO_USER_ERROR)
        resulting_data = self.inspect_user(target_user_hash)
        return resulting_data, target_user.chat_id, self.user.hacker_level <= target_user.hacker_defence

    def prepare_message(self, message):
        self.user_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        message = re.search(r" [a-zA-Z0-9]{10} [\w\W]+$", message).group(0)[12:]
        target_user = self.get_user_by_user_hash(target_user_hash)
        if target_user is None:
            raise UserError(NO_USER_ERROR)
        return target_user.chat_id, message

    def prepare_hacker_message(self, message):
        self.hacker_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        message = re.search(r" [a-zA-Z0-9]{10} [\w\W]+$", message).group(0)[12:]
        target_user = self.get_user_by_user_hash(target_user_hash)
        if target_user is None:
            raise UserError(NO_USER_ERROR)
        return target_user.chat_id, message, self.user.hacker_level <= target_user.hacker_defence

    def set_attribute(self, message):
        self.admin_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        if not target_user:
            raise UserError(NO_USER_ERROR)
        target_attribute = re.search(r"(finances|hacker_level|hacker_defence|is_admin)", message).group(0)
        target_value = int(re.search(r"[0-9]+$",message).group(0))
        User.update_db_value(target_user_hash, target_attribute, target_value, self.database)
        return ATTRIBUTE_UPDATE_MESSAGE

    def create_transaction(self, message):
        self.user_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        message = re.search(r" [a-zA-Z0-9]{10} [\w\W0-9.]+$", message).group(0)[12:]
        def allowed_values(message):
             return all([char.isdigit() or char == '.' for char in message])
        if not allowed_values(message):
            raise TransactionError(TRANSACTION_UNALLOWED_VALUE.substitute(value=message))
        amount = float(message)
        if self.user.finances < amount:
            raise TransactionError(TRANSACTION_NO_FINANCES)
        if not target_user:
            raise TransactionError(TRANSACTION_NO_USER)
        if target_user_hash == self.user.character_hash:
            raise TransactionError(SELF_TRANSACTION)
        if amount <= 0:
            raise TransactionError(ZERO_TRANSACTION)
        transaction_hash = Transaction.create_transaction(self.user.character_hash, target_user_hash, amount, self.database)
        reciever_amount = target_user.finances + amount
        sender_amount = self.user.finances - amount
        User.update_db_value(target_user_hash, "finances", reciever_amount, self.database)
        User.update_db_value(self.user.character_hash, "finances", sender_amount, self.database)
        transaction_message = TRANSACTION_MESSAGE.substitute(
            sender_hash=self.user.character_hash, 
            reciever_hash=target_user_hash,
            amount=amount,
            transaction_hash=transaction_hash
        )
        return self.user.chat_id, target_user.chat_id, transaction_message

    def inspect_transactions(self, is_sender, user_hash=None):
        self.user_validation()
        if user_hash is None:
            user_hash = self.user.character_hash
        transactions = Transaction.list_transactions(user_hash, is_sender, self.database)
        resulting_data = ""
        for transaction in transactions:
            resulting_data += str(transaction) + '\n'
        if not resulting_data:
            resulting_data = NO_TRANSACTIONS_FOUND
        return resulting_data

    def hack_inspect_transactions(self, message, is_sender):
        self.hacker_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        resulting_data = self.inspect_transactions(is_sender, target_user_hash)
        return resulting_data, target_user.chat_id, self.user.hacker_level <= target_user.hacker_defence
