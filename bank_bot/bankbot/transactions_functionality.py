from bank_bot.bankbot.core import bot, client_factory
from bank_bot import settings
from bank_bot.banking_system import UserError, TransactionError, Database, HackerError, MessageError, AddressRecordError

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