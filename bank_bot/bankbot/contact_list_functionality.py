from bank_bot.bankbot.core import bot, client_factory, safe_send_message
from bank_bot import settings
from bank_bot.banking_system import UserError, TransactionError, Database, HackerError, MessageError, AddressRecordError

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
def inspect_contact_list(message):
    client = client_factory.create_client(message)
    try:
        results = client.inspect_contact_list()
    except (UserError, AddressRecordError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    safe_send_message(bot, client.chat_id, results)


