# -*- coding: utf-8 -*-
import telebot

from .banking_system import BankingClientFactory, UserError, TransactionError, Database, HackerError, MessageError, AddressRecordError
from . import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)
database = Database(settings.DATABASE_FILE)
database.initialize_system()
client_factory = BankingClientFactory(database)

# Initial commands

@bot.message_handler(commands=['start',])
def send_welcome(message):
    # Welcome message
    bot.reply_to(message, settings.WELCOME_MESSAGE)

@bot.message_handler(commands=['help',])
def help_message(message):
    # Help command
    bot.reply_to(message, settings.HELP_MESSAGE)

# Registration commands

@bot.message_handler(commands=['create_admin',])
def create_admin(message):
    # Admin creation command; works if user has no registered account in bot and no admins were created.
    client = client_factory.create_client(message)
    try:
        admin_creation_message = client.create_admin()
    except UserError as e:
        admin_creation_message = e.message
    bot.send_message(client.chat_id,admin_creation_message)

@bot.message_handler(regexp=r"^\/register [a-zA-Z0-9а-яА-Я]{1,150}")
def register_user(message):
     # Admin creation command; works if user has no registered account in bot.
    client = client_factory.create_client(message)
    try:
        user_creation_message = client.register_user(message.text)
    except UserError as e:
        user_creation_message = e.message
    bot.send_message(client.chat_id, user_creation_message)
    admin_list = client.get_admins()
    for admin in admin_list:
        bot.send_message(admin.chat_id, user_creation_message)

# Admin commands

@bot.message_handler(commands=['admin_help',])
def admin_help_message(message):
    # Help command
    client = client_factory.create_client(message)
    try:
        client.admin_validation()
        bot.reply_to(message, settings.ADMIN_HELP_MESSAGE)
        return
    except UserError as err:
        bot.send_message(client.chat_id, err.message)
    
@bot.message_handler(regexp=r"^\/delete [a-zA-Z0-9]{10}")
def delete_user(message):
    client = client_factory.create_client(message)
    try:
        message = client.delete_user(message.text)
    except UserError as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(commands=['inspect_all',])
def inspect_all_users(message):
    client = client_factory.create_client(message)
    message = client.inspect_all_users()
    bot.send_message(client.chat_id, message)

@bot.message_handler(regexp=r"^\/set_attribute [a-zA-Z0-9]{10} (finances|hacker_level|hacker_defence|is_admin) [0-9]+")
def set_attribute(message):
    client = client_factory.create_client(message)
    try:
        message = client.set_attribute(message.text)
    except UserError as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(regexp=r"^\/admin_inspect_user [a-zA-Z0-9]{10}")
def admin_inspect_user(message):
    client = client_factory.create_client(message)
    try:
        results = client.admin_inspect_user(message.text)
    except UserError as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/admin_history_sent [a-zA-Z0-9]{10}")
def admin_user_sent_transaction_list(message):
    client = client_factory.create_client(message)
    try:
        results, = client.admin_inspect_transactions(message.text, is_sender=True)
    except (UserError, TransactionError) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/admin_history_recieved [a-zA-Z0-9]{10}")
def admin_user_recieved_transaction_list(message):
    client = client_factory.create_client(message)
    try:
        results, = client.admin_inspect_transactions(message.text, is_sender=False)
    except (UserError, TransactionError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)


@bot.message_handler(regexp=r"^\/admin_history_all [a-zA-Z0-9]{10}")
def admin_list_all_transactions(message):
    client = client_factory.create_client(message)
    try:
        results = client.admin_inspect_all_transactions(message.text)
    except (UserError, TransactionError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/admin_history_pair [a-zA-Z0-9]{10} [a-zA-Z0-9]{10}")
def admin_list_pair_transactions(message):
    client = client_factory.create_client(message)
    try:
        results = client.admin_inspect_pair_history(message.text)
    except (UserError, TransactionError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/admin_history_messages_sent [a-zA-Z0-9]{10}")
def admin_user_sent_messages_list(message):
    client = client_factory.create_client(message)
    try:
        results, = client.admin_inspect_messages(message.text, is_sender=True)
    except (UserError, MessageError) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/admin_history_messages_recieved [a-zA-Z0-9]{10}")
def admin_user_recieved_messages_list(message):
    client = client_factory.create_client(message)
    try:
        results, = client.admin_inspect_messages(message.text, is_sender=False)
    except (UserError, MessageError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)


@bot.message_handler(regexp=r"^\/admin_history_messages_all [a-zA-Z0-9]{10}")
def admin_list_all_messages(message):
    client = client_factory.create_client(message)
    try:
        results = client.admin_inspect_all_messages(message.text)
    except (UserError, MessageError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/admin_history_messages_pair [a-zA-Z0-9]{10} [a-zA-Z0-9]{10}")
def admin_list_pair_messages(message):
    client = client_factory.create_client(message)
    try:
        results = client.admin_inspect_pair_history_messages(message.text)
    except (UserError, MessageError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/admin_add_contact [a-zA-Z0-9]{10} [a-zA-Z0-9]{10} [a-zA-Z0-9а-яА-Я]{1,150}")
def admin_add_contact(message):
    client = client_factory.create_client(message)
    try:
        results = client.admin_add_contact(message.text)
    except (UserError, AddressRecordError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/admin_delete_contact [a-zA-Z0-9]{10} [a-zA-Z0-9]{10}")
def admin_delete_contact(message):
    client = client_factory.create_client(message)
    try:
        results = client.admin_delete_contact(message.text)
    except (UserError, AddressRecordError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/admin_inspect_contact_list [a-zA-Z0-9]{10}")
def admin_inspect_contact_list(message)
    client = client_factory.create_client(message)
    try:
        results = client.admin_inspect_contact_list(message.text)
    except (UserError, AddressRecordError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)
# User self-adressed commands

@bot.message_handler(commands=['inspect',])
def inspect_self(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_self()
    except UserError as err:
        message = err.message
    bot.send_message(client.chat_id, message)

# Communications

@bot.message_handler(regexp=r"\/message [a-zA-Z0-9]{10} [\w\W]+")
def send_message(message):
    # Generic messaging command; allows to send any message to another user registered in bot
    # Only user's unique hash is required to send message; message is signed by sender's hash
    client = client_factory.create_client(message)
    try:
        reciever_chat_id, sent_message = client.prepare_message(message.text)
    except (UserError, MessageError) as err:
        bot.send_message(client.chat_id, err)
        return
    bot.send_message(client.chat_id, f"{settings.MESSAGE_SEND_RESULT} {sent_message}")
    bot.send_message(reciever_chat_id, f"{settings.INCOMING_MESSAGE} {sent_message}.\n{settings.MESSAGE_SENDER} {client.user.character_hash}")

@bot.message_handler(regexp=r"\/admin_hail [\w\W]+")
def admin_hail_users(message):
    client = client_factory.create_client(message)
    try:
        message_list = client.admin_hail_users(message.text)
    except UserError as err:
        bot.send_message(client.chat_id, err)
        return
    for message in message_list:
        bot.send_message(message.chat_id, f"{settings.ADMIN_HAIL_PREFIX}: {message.message}")

@bot.message_handler(commands=['history_messages_sent',])
def list_sent_messages(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_messages(is_sender=True)
    except (UserError, MessageError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(commands=['history_messages_recieved',])
def list_recieved_messages(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_messages(is_sender=False)
    except (UserError, MessageError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(commands=['history_messages',])
def list_all_transactions(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_all_messages()
    except (UserError, MessageError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(regexp=r"^\/history_messages_pair [a-zA-Z0-9]{10}")
def list_pair_transactions(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_pair_history_messages(message=message)
    except (UserError, MessageError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)

# CONTACT LIST
@bot.message_handler(regexp=r"^\/add_contact [a-zA-Z0-9]{10} [a-zA-Z0-9а-яА-Я]{1,150}")
def add_contact(message):
    client = client_factory.create_client(message)
    try:
        results = client.add_contact(message.text)
    except (UserError, AddressRecordError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/delete_contact [a-zA-Z0-9]{10}")
def delete_contact(message):
    client = client_factory.create_client(message)
    try:
        results = client.delete_contact(message.text)
    except (UserError, AddressRecordError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(regexp=r"^\/contact_list")
def inspect_contact_list(message)
    client = client_factory.create_client(message)
    try:
        results = client.inspect_contact_list(message.text)
    except (UserError, AddressRecordError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

# TRANSACTIONS

@bot.message_handler(commands=['history_sent',])
def list_sent_transactions(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_transactions(is_sender=True)
    except (UserError, TransactionError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(commands=['history_recieved',])
def list_recieved_transactions(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_transactions(is_sender=False)
    except (UserError, TransactionError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(commands=['history_all',])
def list_all_transactions(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_all_transactions()
    except (UserError, TransactionError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(regexp=r"^\/history_pair [a-zA-Z0-9]{10}")
def list_pair_transactions(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_pair_history(message=message)
    except (UserError, TransactionError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)


@bot.message_handler(regexp=r"^\/send [a-zA-Z0-9]{10} [0-9.]+")
def create_transaction(message, is_anonymous=False):
    client = client_factory.create_client(message)
    try:
        sender_chat_id, reciever_chat_id, transaction_message = client.create_transaction(message.text)
    except (UserError, TransactionError) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(sender_chat_id, transaction_message)
    if not is_anonymous:
        bot.send_message(reciever_chat_id, transaction_message)
