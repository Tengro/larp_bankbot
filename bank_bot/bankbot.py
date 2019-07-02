# -*- coding: utf-8 -*-
import telebot

from .banking_system import initialize_system, BankingClient, UserError, TransactionError
from . import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)
initialize_system()

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
    client = BankingClient(message)
    try:
        admin_creation_message = client.create_admin()
    except UserError as e:
        admin_creation_message = e.message
    bot.send_message(client.chat_id,admin_creation_message)

@bot.message_handler(regexp=r"^\/register [a-zA-Z0-9а-яА-Я]{1,150}")
def register_user(message):
     # Admin creation command; works if user has no registered account in bot.
    client = BankingClient(message)
    try:
        user_creation_message = bot.send_message(client.chat_id, client.register_user(message.text))
    except UserError as e:
        user_creation_message = bot.send_message(client.chat_id, e.message)
    bot.send_message(client.chat_id, user_creation_message)
    # TODO: Add Admin notification of registration

# Admin commands

@bot.message_handler(commands=['admin_help',])
def admin_help_message(message):
    # Help command
    client = BankingClient(message)
    try:
        client.admin_validation()
        bot.reply_to(message, settings.ADMIN_HELP_MESSAGE)
        return
    except UserError as err:
        bot.send_message(client.chat_id, err.message)

@bot.message_handler(commands=['hacker_help',])
def admin_help_message(message):
    # Help command
    client = BankingClient(message)
    try:
        client.hacker_validation()
        bot.reply_to(message, settings.HACKER_HELP_MESSAGE)
        return
    except UserError as err:
        bot.send_message(client.chat_id, err.message)
    

@bot.message_handler(regexp=r"^\/delete [a-zA-Z0-9]{10}")
def delete_user(message):
    client = BankingClient(message)
    try:
        message = client.delete_user(message.text)
    except UserError as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(commands=['inspect_all',])
def inspect_all_users(message):
    client = BankingClient(message)
    try:
        message = client.inspect_all_users(message.text)
    except UserError as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(regexp=r"^\/set_attribute [a-zA-Z0-9]{10} (finances|hacker_level|hacker_defence|is_admin) [0-9]+")
def set_attribute(message):
    client = BankingClient(message)
    try:
        message = client.set_attribute(message.text)
    except UserError as err:
        message = err.message
    bot.send_message(client.chat_id, message)

# User self-adressed commands

@bot.message_handler(commands=['inspect',])
def inspect_self(message):
    client = BankingClient(message)
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
    client = BankingClient(message)
    try:
        reciever_chat_id, sent_message = client.prepare_message(message.text)
    except UserError as err:
        bot.send_message(client.chat_id, err)
        return
    bot.send_message(client.chat_id, f"{settings.MESSAGE_SEND_RESULT}: {sent_message}")
    bot.send_message(reciever_chat_id, f"{settings.INCOMING_MESSAGE} {client.user.character_hash}: {sent_message}")

# TRANSACTIONS

@bot.message_handler(commands=['list_sent',])
def list_sent_transactions(message):
    client = BankingClient(message)
    try:
        message = client.inspect_transactions(is_sender=True)
    except (UserError, TransactionError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)

@bot.message_handler(commands=['list_recieved',])
def list_recieved_transactions(message):
    client = BankingClient(message)
    try:
        message = client.inspect_transactions(is_sender=False)
    except (UserError, TransactionError) as err:
        message = err.message
    bot.send_message(client.chat_id, message)


@bot.message_handler(regexp=r"^\/send [a-zA-Z0-9]{10} [0-9]+")
def create_transaction(message, is_anonymous=False):
    client = BankingClient(message)
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
        client = BankingClient(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_user(message.text)
        except UserError as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.USER_DATA, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)


    @bot.message_handler(regexp=r"^\/h@ck_list_sent [a-zA-Z0-9]{10}")
    def hack_user_sent_transaction_list(message):
        client = BankingClient(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_transactions(message.text, is_sender=True)
        except (UserError, TransactionError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.SENT_TRANSACTIONS_DATA, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)

    @bot.message_handler(regexp=r"^\/h@ck_list_recieved [a-zA-Z0-9]{10}")
    def hack_user_recieved_transaction_list(message):
        client = BankingClient(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_transactions(message.text, is_sender=False)
        except (UserError, TransactionError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.RECIEVED_TRANSACTIONS_DATA, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)

    @bot.message_handler(regexp=r"\/mess@ge [a-zA-Z0-9]{10} [\w\W]+")
    def send_hacked_message(message):
        client = BankingClient(message)
        try:
            reciever_chat_id, sent_message, show_sender = client.prepare_hacker_message(message.text)
        except UserError as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, f"{settings.MESSAGE_SEND_RESULT}: {sent_message}")
        if show_sender:
            bot.send_message(reciever_chat_id, f"{settings.INCOMING_MESSAGE} {client.user.character_hash}: {sent_message}")
        else:
            bot.send_message(reciever_chat_id, f"{settings.INCOMING_MESSAGE}: {sent_message}")

