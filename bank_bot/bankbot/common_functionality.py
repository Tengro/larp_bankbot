from bank_bot.bankbot.core import bot, client_factory
from bank_bot import settings
from bank_bot.banking_system import UserError, TransactionError, Database, HackerError, MessageError, AddressRecordError

@bot.message_handler(commands=['start',])
def send_welcome(message):
    # Welcome message
    bot.reply_to(message, settings.WELCOME_MESSAGE)

@bot.message_handler(commands=['help',])
def help_message(message):
    # Help command
    bot.reply_to(message, settings.HELP_MESSAGE)

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

@bot.message_handler(commands=['inspect',])
def inspect_self(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_self()
    except UserError as err:
        message = err.message
    bot.send_message(client.chat_id, message)
