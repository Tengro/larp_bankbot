from bank_bot.bankbot.core import bot, client_factory, safe_send_message
from bank_bot import settings
from bank_bot.banking_system import UserError, TransactionError, Database, HackerError, MessageError, AddressRecordError

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
    safe_send_message(bot, client.chat_id, f"{settings.MESSAGE_SEND_RESULT} {sent_message}")
    safe_send_message(bot, reciever_chat_id, f"{settings.INCOMING_MESSAGE} {sent_message}.\n{settings.MESSAGE_SENDER} {client.user.character_hash}")


@bot.message_handler(commands=['history_messages_sent',])
def list_sent_messages(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_messages(is_sender=True)
    except (UserError, MessageError) as err:
        message = err.message
    safe_send_message(bot, client.chat_id, message)

@bot.message_handler(commands=['history_messages_recieved',])
def list_recieved_messages(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_messages(is_sender=False)
    except (UserError, MessageError) as err:
        message = err.message
    safe_send_message(bot, client.chat_id, message)

@bot.message_handler(commands=['history_messages',])
def list_all_messages(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_all_messages()
    except (UserError, MessageError) as err:
        message = err.message
    safe_send_message(bot, client.chat_id, message)

@bot.message_handler(regexp=r"^\/history_messages_pair [a-zA-Z0-9]{10}")
def list_pair_messages(message):
    client = client_factory.create_client(message)
    try:
        message = client.inspect_pair_history_messages(message=message.text)
    except (UserError, MessageError) as err:
        message = err.message
    safe_send_message(bot, client.chat_id, message)
