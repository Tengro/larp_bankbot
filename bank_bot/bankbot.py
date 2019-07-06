# -*- coding: utf-8 -*-
import telebot

from .banking_system import BankingClientFactory, UserError, TransactionError, Database, HackerError
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

@bot.message_handler(commands=['hacker_help',])
def hacker_help_message(message):
    # Help command
    client = client_factory.create_client(message)
    try:
        client.hacker_validation()
        bot.reply_to(message, settings.HACKER_HELP_MESSAGE)
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
    except UserError as err:
        bot.send_message(client.chat_id, err)
        return
    bot.send_message(client.chat_id, f"{settings.MESSAGE_SEND_RESULT}: {sent_message}")
    bot.send_message(reciever_chat_id, f"{settings.INCOMING_MESSAGE}: {sent_message}. {settings.MESSAGE_SENDER}")
    bot.send_message(reciever_chat_id, f"{client.user.character_hash}")

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


@bot.message_handler(regexp=r"^\/send [a-zA-Z0-9]{10} [\w\W0-9.]+")
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


# HACK_SUBSYSTEM
if settings.HACKING_ALLOWED:
    @bot.message_handler(regexp=r"^\/h@ck_user [a-zA-Z0-9]{10}")
    def hack_user(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_user(message.text)
        except (UserError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.USER_DATA, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)


    @bot.message_handler(regexp=r"^\/h@ck_history_sent [a-zA-Z0-9]{10}")
    def hack_user_sent_transaction_list(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_transactions(message.text, is_sender=True)
        except (UserError, TransactionError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.SENT_TRANSACTIONS_DATA, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)

    @bot.message_handler(regexp=r"^\/h@ck_history_recieved [a-zA-Z0-9]{10}")
    def hack_user_recieved_transaction_list(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_transactions(message.text, is_sender=False)
        except (UserError, TransactionError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.RECIEVED_TRANSACTIONS_DATA, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)

    @bot.message_handler(regexp=r"\/h@ck_message [a-zA-Z0-9]{10} [\w\W]+")
    def send_hacked_message(message):
        client = client_factory.create_client(message)
        try:
            reciever_chat_id, sent_message, show_sender = client.prepare_hacker_message(message.text)
        except (UserError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, f"{settings.MESSAGE_SEND_RESULT} {sent_message}")
        if show_sender:
            bot.send_message(reciever_chat_id, f"{settings.INCOMING_MESSAGE} {sent_message}. {settings.MESSAGE_SENDER}")
            bot.send_message(reciever_chat_id, f"{client.user.character_hash}")
        else:
            bot.send_message(reciever_chat_id, f"{settings.INCOMING_MESSAGE} {sent_message}. {settings.MESSAGE_SENDER}")
            bot.send_message(reciever_chat_id, f"{settings.ANON_USER}")

    @bot.message_handler(regexp=r"^\/h@ck_history_all [a-zA-Z0-9]{10}")
    def hack_list_all_transactions(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_all_transactions(message)
        except (UserError, TransactionError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.TRANSACTIONS_DATA_HISTORY, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)

    @bot.message_handler(regexp=r"^\/h@ck_history_pair [a-zA-Z0-9]{10} [a-zA-Z0-9]{10}")
    def hack_list_pair_transactions(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, victim_hash, second_victim_chat_id, second_victim_hash, show_sender = client.hack_inspect_pair_history(message)
        except (UserError, TransactionError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            first_transaction_pair = TRANSACTION_PAIR.substitute(second_user=second_victim_hash)
            second_transaction_pair = TRANSACTION_PAIR.substitute(second_user=victim_hash)
            hack_message_first = settings.HACK_ALERT.substitute(data_type=first_transaction_pair, hacker_hash=client.user.character_hash)
            hack_message_second = settings.HACK_ALERT.substitute(data_type=second_transaction_pair, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message_first)
            bot.send_message(second_victim_chat_id, hack_message_second)


