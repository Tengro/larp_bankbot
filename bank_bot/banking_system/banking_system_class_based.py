import re
from collections import namedtuple

from bank_bot.settings import (
    DATETIME_FORMAT, NO_USER_ERROR, NO_ADMIN_ERROR, ALREADY_ADMIN,
    ADMIN_RECORD_CREATED, ALREADY_REGISTERED, NO_NAME, REGISTRATION_MESSAGE,
    DELETION_MESSAGE, TRANSACTION_NO_FINANCES, TRANSACTION_MESSAGE,
    NO_TRANSACTIONS_FOUND, ATTRIBUTE_UPDATE_MESSAGE,
    ALREADY_HAVE_USER,ZERO_TRANSACTION, SELF_TRANSACTION, TRANSACTION_UNALLOWED_VALUE,
    HACKER_TOO_PROTECTED, HACKING_ALLOWED, NO_HACKING_ALLOWED_ERROR, NO_MESSAGES_FOUND,
    NO_ADDRESS_RECORDS, NO_SELF_MESSAGING, NO_SELF_ADDRESSING, ADDRESS_RECORD_ADDED,
    ADDRESS_RECORD_DELETION_MESSAGE, NO_DUPLICATES, HACKER_MESSAGE_DIFFICULY, HACKER_COMMON_DIFFICULTY,
    HACKER_TRANSACTION_DIFFICULTY, HACKER_THEFT_DIFFICULTY,HACKER_FAKE_HASH
)

from bank_bot.banking_system.user_class import User
from bank_bot.banking_system.transaction_class import Transaction
from bank_bot.banking_system.message_class import Message
from bank_bot.banking_system.address_record_class import AddressRecord
from bank_bot.banking_system.exceptions import TransactionError, UserError, HackerError, MessageError, AddressRecordError
from bank_bot.banking_system.csv_parsers import mass_set_character_csv, mass_set_contact_csv


class BankingClient(object):
    def __init__(self, message, database):
        if hasattr(message, 'json'):
            self.user_id = str(message.json['from']['id'])
            self.chat_id = str(message.json['chat']['id'])
        else:
            self.user_id = None
            self.chat_id = None            
        self.database = database
        self.user = self.get_user_by_id(self.user_id)


# COMMON FUNCTIONALITY
    def get_user_by_id(self, user_id):
        user = User.get_user_by_id(user_id, self.database)
        return user

    def get_user_by_name(self, user_name):
        user = User.get_user_by_name(user_name, self.database)
        return user

    def get_user_by_user_hash(self, character_hash):
        user = User.get_user_by_user_hash(character_hash, self.database)
        if not user:
            raise UserError(NO_USER_ERROR)
        return user

    def get_admins(self):
        admin_list = User.get_admin_list(self.database)
        return admin_list

    def admin_validation(self):
        self.user_validation()
        if not self.user.is_admin:
            raise UserError(NO_ADMIN_ERROR)

    def user_validation(self):
        if self.user is None:
            raise UserError(NO_USER_ERROR)

    def hacker_validation(self, hacker_defence=0):
        if not HACKING_ALLOWED:
            raise HackerError(NO_HACKING_ALLOWED_ERROR)
        self.user_validation()
        if self.user.hacker_level < hacker_defence or self.user.hacker_level == 0:
            raise HackerError(HACKER_TOO_PROTECTED)
        return self.user.hacker_level == hacker_defence

    def inspect_user(self, user_hash=None):
        self.user_validation()
        if user_hash is None:
            user_hash = self.user.character_hash
        user = self.get_user_by_user_hash(user_hash)
        return str(user)

# ADMIN FUNCTIONALITY
    def create_admin(self):
        if self.user is not None:
            raise UserError(ALREADY_ADMIN)
        user = User.create_admin(self.user_id, self.chat_id, self.database)
        return ADMIN_RECORD_CREATED

    def admin_hail_users(self, message):
        self.admin_validation()
        message = re.search(r" [\w\W]+$", message).group(0).strip(' ')
        all_users = User.inspect_all_users(self.database)
        MessageData = namedtuple("MessageData", "chat_id,message")
        resulting_list = [MessageData._make([user.chat_id, message]) for user in all_users if user.is_admin == 0]
        return resulting_list

    def inspect_all_users(self):
        self.admin_validation()
        all_users = User.inspect_all_users(self.database)
        resulting_data = ""
        for user in all_users:
            resulting_data += str(user) + '\n\n'
        return resulting_data

    def set_attribute(self, message):
        self.admin_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        target_attribute = re.search(r"(finances|hacker_level|hacker_defence|is_admin)", message).group(0)
        target_value = int(re.search(r"[0-9]+$",message).group(0))
        User.update_db_value(target_user_hash, target_attribute, target_value, self.database)
        return ATTRIBUTE_UPDATE_MESSAGE

    def delete_user(self, message_text):
        self.admin_validation()
        target_user_hash = message_text.strip('/delete ')
        user = User.delete_by_hash(target_user_hash, self.database)
        return DELETION_MESSAGE.substitute(character_hash=target_user_hash)

    def admin_inspect_user(self, message):
        self.admin_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        resulting_data = self.inspect_user(target_user_hash)
        return resulting_data

    def admin_inspect_pair_history(self, message):
        self.admin_validation()
        target_first_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        target_second_user_hash = re.search(r" [a-zA-Z0-9]{10}$", message).group(0).strip(' ')
        resulting_data = self.inspect_pair_history(message, target_first_user_hash, target_second_user_hash)
        return resulting_data

    def admin_inspect_all_transactions(self, message):
        self.admin_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        resulting_data = self.inspect_all_transactions(target_user_hash)
        return resulting_data
        
    def admin_inspect_transactions(self, message, is_sender):
        self.admin_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        resulting_data = self.inspect_transactions(is_sender, target_user_hash)
        return resulting_data

    def admin_inspect_messages(self, message, is_sender):
        self.admin_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        resulting_data = self.inspect_messages(is_sender, target_user_hash)
        return resulting_data

    def admin_inspect_all_messages(self, message):
        self.admin_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        resulting_data = self.inspect_all_messages(target_user_hash)
        return resulting_data

    def admin_inspect_pair_history_messages(self, message, sender_hash=None, reciever_hash=None):
        self.admin_validation()
        target_first_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        target_second_user_hash = re.search(r" [a-zA-Z0-9]{10}$", message).group(0).strip(' ')
        resulting_data = self.inspect_pair_history_messages(message, target_first_user_hash, target_second_user_hash)
        return resulting_data

    def admin_add_contact(self, message, owner_hash=None):
        self.admin_validation()
        target_hashes = re.findall(r"[a-zA-Z0-9]{10}", message)
        target_first_user_hash = target_hashes[0]
        target_second_user_hash = target_hashes[1]
        first_target_user = self.get_user_by_user_hash(target_first_user_hash)
        second_target_user = self.get_user_by_user_hash(target_second_user_hash)
        target_user_name = re.search(r"[a-zA-Z0-9]{10} [a-zA-Z0-9]{10} [\w\W]+$", message).group(0)[22:]
        address_records = AddressRecord.list_address_records(target_first_user_hash, self.database)
        existing_records = [x.target_hash for x in address_records]
        if target_second_user_hash == target_first_user_hash:
            raise AddressRecordError(NO_SELF_ADDRESSING)
        if target_second_user_hash in existing_records:
            raise AddressRecordError(NO_DUPLICATES)
        AddressRecord.create_address_record(target_first_user_hash, target_second_user_hash, target_user_name, self.database)
        return ADDRESS_RECORD_ADDED

    def admin_delete_contact(self, message, user_hash=None):
        self.admin_validation()
        target_hashes = re.findall(r"[a-zA-Z0-9]{10}", message)
        target_first_user_hash = target_hashes[0]
        target_second_user_hash = target_hashes[1]
        first_target_user = self.get_user_by_user_hash(target_first_user_hash)
        second_target_user = self.get_user_by_user_hash(target_second_user_hash)
        AddressRecord.delete_address_record(target_first_user_hash, target_second_user_hash, self.database)
        return ADDRESS_RECORD_DELETION_MESSAGE

    def admin_inspect_contact_list(self, message):
        self.admin_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        return self.inspect_contact_list(target_user_hash)

    def admin_mass_set_character_csv(self, document):
        self.admin_validation()
        good_result_counter, total_result_counter, error_list = mass_set_character_csv(document, self.database)
        error_list_formatted = '\n'.join(error_list)
        results = f"OK: {good_result_counter} of {total_result_counter}; errors:\n {error_list_formatted}"
        return results

    def admin_mass_set_contact_csv(self, document):
        self.admin_validation()
        results = mass_set_contact_csv(document, self.database)
        error_list_formatted = '\n'.join(error_list)
        results = f"OK: {good_result_counter} of {total_result_counter}; errors:\n {error_list_formatted}"
        return results

# USER FUNCTIONALITY
    def inspect_self(self):
        return self.inspect_user()

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

    def create_transaction(self, message):
        self.user_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        message = re.search(r" [a-zA-Z0-9]{10} [\w\W0-9.]+$", message).group(0)[12:].strip(' ')
        def allowed_values(message):
             return all([char.isdigit() or char == '.' for char in message])
        if not allowed_values(message):
            raise TransactionError(TRANSACTION_UNALLOWED_VALUE.substitute(value=message))
        amount = float(message)
        if self.user.finances < amount:
            raise TransactionError(TRANSACTION_NO_FINANCES)
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
            resulting_data += str(transaction) + '\n\n'
        if not transactions:
            resulting_data = NO_TRANSACTIONS_FOUND
        return resulting_data

    def inspect_all_transactions(self, user_hash=None):
        self.user_validation()
        if user_hash is None:
            user_hash = self.user.character_hash
        transactions = Transaction.list_all_transactions(user_hash, self.database)
        resulting_data = ""
        for transaction in transactions:
            resulting_data += str(transaction) + '\n\n'
        if not transactions:
            resulting_data = NO_TRANSACTIONS_FOUND
        return resulting_data

    def inspect_pair_history(self, message, sender_hash=None, reciever_hash=None):
        self.user_validation()
        if sender_hash is None:
            sender_hash = self.user.character_hash
        if reciever_hash is None:
            reciever_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        transactions = Transaction.list_pair_history_transactions(sender_hash, reciever_hash, self.database)
        resulting_data = ""
        for transaction in transactions:
            resulting_data += str(transaction) + '\n\n'
        if not transactions:
            resulting_data = NO_TRANSACTIONS_FOUND
        return resulting_data

# MESSAGING FUNCTIONALITY
    def prepare_message(self, message):
        self.user_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        message = re.search(r" [a-zA-Z0-9]{10} [\w\W]+$", message).group(0)[12:]
        target_user = self.get_user_by_user_hash(target_user_hash)
        if target_user_hash == self.user.character_hash:
            raise MessageError(NO_SELF_MESSAGING)
        Message.create_message(self.user.character_hash, target_user_hash, message, self.database)
        return target_user.chat_id, message

    def inspect_messages(self, is_sender, user_hash=None):
        self.user_validation()
        if user_hash is None:
            user_hash = self.user.character_hash
        messages = Message.inspect_messages(user_hash, is_sender, self.database)
        resulting_data = ""
        for message in messages:
            resulting_data += str(message) + '\n'
        if not messages:
            resulting_data = NO_MESSAGES_FOUND
        return resulting_data

    def inspect_all_messages(self, user_hash=None):
        self.user_validation()
        if user_hash is None:
            user_hash = self.user.character_hash
        messages = Message.inspect_all_messages(user_hash, self.database)
        resulting_data = ""
        for message in messages:
            resulting_data += str(message) + '\n'
        if not messages:
            resulting_data = NO_MESSAGES_FOUND
        return resulting_data

    def inspect_pair_history_messages(self, message, sender_hash=None, reciever_hash=None):
        self.user_validation()
        if sender_hash is None:
            sender_hash = self.user.character_hash
        if reciever_hash is None:
            reciever_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        messages = Message.inspect_pair_history_messages(sender_hash, reciever_hash, self.database)
        resulting_data = ""
        for message in messages:
            resulting_data += str(message) + '\n\n'
        if not messages:
            resulting_data = NO_MESSAGES_FOUND
        return resulting_data

#CONTACT LIST FUNCTIONALITY
    def add_contact(self, message, owner_hash=None):
        self.user_validation()
        if owner_hash is None:
            owner_hash = self.user.character_hash
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user_name = re.search(r" [a-zA-Z0-9]{10} [\w\W]+$", message).group(0)[12:]
        target_user = self.get_user_by_user_hash(target_user_hash)
        address_records = AddressRecord.list_address_records(owner_hash, self.database)
        existing_records = [x.target_hash for x in address_records]
        if target_user_hash == owner_hash:
            raise AddressRecordError(NO_SELF_ADDRESSING)
        if target_user_hash in existing_records:
            raise AddressRecordError(NO_DUPLICATES)
        AddressRecord.create_address_record(owner_hash, target_user_hash, target_user_name, self.database)
        return ADDRESS_RECORD_ADDED

    def delete_contact(self, message, user_hash=None):
        self.user_validation()
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        if user_hash is None:
            user_hash = self.user.character_hash
        AddressRecord.delete_address_record(user_hash, target_user_hash, self.database)
        return ADDRESS_RECORD_DELETION_MESSAGE

    def inspect_contact_list(self, user_hash=None):
        self.user_validation()
        if user_hash is None:
            user_hash = self.user.character_hash
        address_records = AddressRecord.list_address_records(user_hash, self.database)
        resulting_data = ""
        for address_record in address_records:
            resulting_data += str(address_record) + '\n'
        if not address_records:
            resulting_data = NO_ADDRESS_RECORDS
        return resulting_data

# HACKER FUNCTIONALITY
    def hack_inspect_user(self, message):
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        show_hack = self.hacker_validation(target_user.hacker_defence + HACKER_COMMON_DIFFICULTY)
        resulting_data = self.inspect_user(target_user_hash)
        return resulting_data, target_user.chat_id, self.user.hacker_level == target_user.hacker_defence

    def hack_inspect_transactions(self, message, is_sender):
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        resulting_data = self.inspect_transactions(is_sender, target_user_hash)
        show_hack = self.hacker_validation(target_user.hacker_defence + HACKER_TRANSACTION_DIFFICULTY)
        return resulting_data, target_user.chat_id, self.user.hacker_level == target_user.hacker_defence

    def hack_inspect_pair_history(self, message):
        target_first_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        target_second_user_hash = re.search(r" [a-zA-Z0-9]{10}$", message).group(0).strip(' ')
        first_target_user = self.get_user_by_user_hash(target_first_user_hash)
        second_target_user = self.get_user_by_user_hash(target_second_user_hash)
        lesser_defence = min(first_target_user.hacker_defence, second_target_user.hacker_defence)
        show_hack = self.hacker_validation(lesser_defence + HACKER_TRANSACTION_DIFFICULTY)
        resulting_data = self.inspect_pair_history(message, target_first_user_hash, target_second_user_hash)
        return resulting_data, first_target_user.chat_id, target_first_user_hash,  second_target_user.chat_id, target_second_user_hash, show_hack

    def hack_inspect_all_transactions(self, message):
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        show_hack = self.hacker_validation(target_user.hacker_defence + HACKER_TRANSACTION_DIFFICULTY)
        resulting_data = self.inspect_all_transactions(target_user_hash)
        return resulting_data, target_user.chat_id, show_hack

    def hack_inspect_messages(self, message, is_sender):
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        resulting_data = self.inspect_messages(is_sender, target_user_hash)
        show_hack = self.hacker_validation(target_user.hacker_defence + HACKER_MESSAGE_DIFFICULY)
        return resulting_data, target_user.chat_id, show_hack

    def hack_inspect_pair_history_messages(self, message):
        target_first_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        target_second_user_hash = re.search(r" [a-zA-Z0-9]{10}$", message).group(0).strip(' ')
        first_target_user = self.get_user_by_user_hash(target_first_user_hash)
        second_target_user = self.get_user_by_user_hash(target_second_user_hash)
        lesser_defence = min(first_target_user.hacker_defence, second_target_user.hacker_defence)
        show_hack = self.hacker_validation(lesser_defence + HACKER_MESSAGE_DIFFICULY)
        resulting_data = self.inspect_pair_history_messages(message, target_first_user_hash, target_second_user_hash)
        return resulting_data, first_target_user.chat_id, target_first_user_hash,  second_target_user.chat_id, target_second_user_hash, show_hack

    def hack_inspect_all_messages(self, message):
        target_user_hash = re.search(r" [a-zA-Z0-9]{10}", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)     
        resulting_data = self.inspect_all_messages(target_user_hash)
        show_hack = self.hacker_validation(target_user.hacker_defence + HACKER_MESSAGE_DIFFICULY)
        return resulting_data, target_user.chat_id, show_hack

    def prepare_hacker_message(self, message):
        target_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        message = re.search(r" [a-zA-Z0-9]{10} [\w\W]+$", message).group(0)[12:]
        self.user_validation()
        target_user = self.get_user_by_user_hash(target_user_hash)
        if target_user_hash == self.user.character_hash:
            raise MessageError(NO_SELF_MESSAGING)
        show_hack = self.hacker_validation(target_user.hacker_defence + HACKER_MESSAGE_DIFFICULY)
        if show_hack:
            Message.create_message(self.user.character_hash, target_user_hash, message, self.database)
        else:
            Message.create_message(self.user.character_hash, HACKER_FAKE_HASH, message, self.database)
            Message.create_message(HACKER_FAKE_HASH, target_user_hash, message, self.database)
        return target_user.chat_id, message, show_hack

    def create_hacker_transaction(self, message):
        target_user_hash = re.search(r" [a-zA-Z0-9]{10} ", message).group(0).strip(' ')
        target_user = self.get_user_by_user_hash(target_user_hash)
        hacker_user = self.get_user_by_user_hash(self.user.character_hash)
        message = re.search(r" [a-zA-Z0-9]{10} [\w\W0-9.]+$", message).group(0)[12:].strip(' ')
        show_hack = self.hacker_validation(target_user.hacker_defence + HACKER_THEFT_DIFFICULTY)
        def allowed_values(message):
             return all([char.isdigit() or char == '.' for char in message])
        if not allowed_values(message):
            raise TransactionError(TRANSACTION_UNALLOWED_VALUE.substitute(value=message))
        amount = float(message)
        if self.user.finances < amount:
            raise TransactionError(TRANSACTION_NO_FINANCES)
        if target_user_hash == self.user.character_hash:
            raise TransactionError(SELF_TRANSACTION)
        if amount <= 0:
            raise TransactionError(ZERO_TRANSACTION)
        if show_hack:
            transaction_hash = Transaction.create_transaction(target_user_hash, self.user.character_hash, amount, self.database)
        else:
            transaction_hash_out = Transaction.create_transaction(target_user_hash, HACKER_FAKE_HASH, amount, self.database)
            transaction_hash_in = Transaction.create_transaction(HACKER_FAKE_HASH, self.user.character_hash, amount, self.database)
            transaction_hash = transaction_hash_out + ' ' + transaction_hash_in
        reciever_amount =  hacker_user.finances + amount
        sender_amount = target_user.finances - amount
        User.update_db_value(target_user_hash, "finances", sender_amount, self.database)
        User.update_db_value(hacker_user.character_hash, "finances", reciever_amount, self.database)
        transaction_message = TRANSACTION_MESSAGE.substitute(
            sender_hash=target_user_hash, 
            reciever_hash=hacker_user.character_hash,
            amount=amount,
            transaction_hash=transaction_hash
        )
        return hacker_user.chat_id, hacker_user.character_hash, target_user.chat_id, transaction_message, show_hack

    def create_hacker_transaction_other(self, message):
        target_hashes = re.findall(r"[a-zA-Z0-9]{10}", message)
        target_first_user_hash = target_hashes[0]
        target_second_user_hash = target_hashes[1]
        target_user = self.get_user_by_user_hash(target_first_user_hash)
        reciever_user = self.get_user_by_user_hash(target_second_user_hash)

        message = re.search(r" [a-zA-Z0-9]{10} [a-zA-Z0-9]{10} [\w\W0-9.]+$", message).group(0)[22:].strip(' ')
        show_hack = self.hacker_validation(target_user.hacker_defence + HACKER_THEFT_DIFFICULTY)
        def allowed_values(message):
             return all([char.isdigit() or char == '.' for char in message])
        if not allowed_values(message):
            raise TransactionError(TRANSACTION_UNALLOWED_VALUE.substitute(value=message))
        amount = float(message)
        if self.user.finances < amount:
            raise TransactionError(TRANSACTION_NO_FINANCES)
        if target_first_user_hash == self.user.character_hash:
            raise TransactionError(SELF_TRANSACTION)
        if amount <= 0:
            raise TransactionError(ZERO_TRANSACTION)
        if show_hack:
            transaction_hash = Transaction.create_transaction(target_first_user_hash, target_second_user_hash, amount, self.database)
        else:
            transaction_hash_out = Transaction.create_transaction(target_first_user_hash, HACKER_FAKE_HASH, amount, self.database)
            transaction_hash_in = Transaction.create_transaction(HACKER_FAKE_HASH, target_second_user_hash, amount, self.database)
            transaction_hash = transaction_hash_out + ' ' + transaction_hash_in
        reciever_amount =  reciever_user.finances + amount
        sender_amount = target_user.finances - amount
        User.update_db_value(target_first_user_hash, "finances", sender_amount, self.database)
        User.update_db_value(target_second_user_hash, "finances", reciever_amount, self.database)
        transaction_message = TRANSACTION_MESSAGE.substitute(
            sender_hash=target_first_user_hash, 
            reciever_hash=target_second_user_hash,
            amount=amount,
            transaction_hash=transaction_hash
        )
        return self.user.character_hash, target_user.chat_id, reciever_user.chat_id, transaction_message, show_hack
