from bank_bot.bankbot.core import bot, client_factory
from bank_bot import settings
from bank_bot.banking_system import UserError, TransactionError, Database, HackerError, MessageError, AddressRecordError

# HACK_SUBSYSTEM
@bot.message_handler(commands=['hacker_help',])
def hacker_help_message(message):
    # Help command
    client = client_factory.create_client(message)
    try:
        client.hacker_validation()
        bot.reply_to(message, settings.HACKER_HELP_MESSAGE)
        return
    except (UserError, HackerError) as err:
        bot.send_message(client.chat_id, err.message)
        return

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

    @bot.message_handler(regexp=r"^\/h@ck_history_all [a-zA-Z0-9]{10}")
    def hack_list_all_transactions(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_all_transactions(message.text)
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
            results, victim_chat_id, victim_hash, second_victim_chat_id, second_victim_hash, show_sender = client.hack_inspect_pair_history(message.text)
        except (UserError, TransactionError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            first_transaction_pair = settings.TRANSACTION_PAIR.substitute(second_user=second_victim_hash)
            second_transaction_pair = settings.TRANSACTION_PAIR.substitute(second_user=victim_hash)
            hack_message_first = settings.HACK_ALERT.substitute(data_type=first_transaction_pair, hacker_hash=client.user.character_hash)
            hack_message_second = settings.HACK_ALERT.substitute(data_type=second_transaction_pair, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message_first)
            bot.send_message(second_victim_chat_id, hack_message_second)

    @bot.message_handler(regexp=r"^\/h@ck_history_messages_sent [a-zA-Z0-9]{10}")
    def hack_user_sent_transaction_list(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_messages(message.text, is_sender=True)
        except (UserError, TransactionError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.SENT_MESSAGES_DATA, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)

    @bot.message_handler(regexp=r"^\/h@ck_history_messages_recieved [a-zA-Z0-9]{10}")
    def hack_user_recieved_transaction_list(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_messages(message.text, is_sender=False)
        except (UserError, MessageError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.RECIEVED_MESSAGES_DATA, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)

    @bot.message_handler(regexp=r"^\/h@ck_history_messages [a-zA-Z0-9]{10}")
    def hack_list_all_transactions(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, show_sender = client.hack_inspect_all_messages(message.text)
        except (UserError, MessageError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            hack_message = settings.HACK_ALERT.substitute(data_type=settings.MESSAGES_DATA_HISTORY, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message)

    @bot.message_handler(regexp=r"^\/h@ck_history_messages_pair [a-zA-Z0-9]{10} [a-zA-Z0-9]{10}")
    def hack_list_pair_transactions(message):
        client = client_factory.create_client(message)
        try:
            results, victim_chat_id, victim_hash, second_victim_chat_id, second_victim_hash, show_sender = client.hack_inspect_pair_history_messages(message.text)
        except (UserError, MessageError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(client.chat_id, results)
        if show_sender:
            first_transaction_pair = settings.MESSAGES_PAIR.substitute(second_user=second_victim_hash)
            second_transaction_pair = settings.MESSAGES_PAIR.substitute(second_user=victim_hash)
            hack_message_first = settings.HACK_ALERT.substitute(data_type=first_transaction_pair, hacker_hash=client.user.character_hash)
            hack_message_second = settings.HACK_ALERT.substitute(data_type=second_transaction_pair, hacker_hash=client.user.character_hash)
            bot.send_message(victim_chat_id, hack_message_first)
            bot.send_message(second_victim_chat_id, hack_message_second)

    @bot.message_handler(regexp=r"^\/h@ck_theft_other [a-zA-Z0-9]{10} [a-zA-Z0-9]{10} [0-9.]+")
    def create_hacked_transaction_other(message):
        client = client_factory.create_client(message)
        try:
            hacker_hash, victim_chat_id, reciever_chat_id, transaction_message, show_hack = client.create_hacker_transaction_other(message.text)
        except (UserError, TransactionError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(reciever_chat_id, transaction_message)
        if show_hack:
            hack_message = settings.HACK_THEFT_ALERT.substitute(hacker_hash=hacker_hash)
            bot.send_message(victim_chat_id, transaction_message)
            bot.send_message(victim_chat_id, hack_message)

    @bot.message_handler(regexp=r"\/h@ck_message [a-zA-Z0-9]{10} [\w\W]+")
    def send_hacked_message(message):
        # Generic messaging command; allows to send any message to another user registered in bot
        # Only user's unique hash is required to send message; message is signed by sender's hash\
        client = client_factory.create_client(message)
        try:
            reciever_chat_id, sent_message, show_hack = client.prepare_hacker_message(message.text)
        except (UserError, MessageError, HackerError) as err:
            bot.send_message(client.chat_id, err)
            return
        bot.send_message(client.chat_id, f"{settings.MESSAGE_SEND_RESULT} {sent_message}")
        if show_hack:
            bot.send_message(reciever_chat_id, f"{settings.INCOMING_MESSAGE} {sent_message}.\n{settings.MESSAGE_SENDER} {client.user.character_hash}")
        else:
            bot.send_message(reciever_chat_id, f"{settings.INCOMING_MESSAGE} {sent_message}.\n{settings.MESSAGE_SENDER} {settings.HACKER_FAKE_HASH}")

    @bot.message_handler(regexp=r"^\/h@ck_theft [a-zA-Z0-9]{10} [0-9.]+")
    def create_hacked_transaction(message):
        client = client_factory.create_client(message)
        try:
            hacker_chat_id, hacker_hash, victim_chat_id, transaction_message, show_hack = client.create_hacker_transaction(message.text)
        except (UserError, TransactionError, HackerError) as err:
            bot.send_message(client.chat_id, err.message)
            return
        bot.send_message(hacker_chat_id, transaction_message)
        if show_hack:
            hack_message = settings.HACK_THEFT_ALERT.substitute(hacker_hash=hacker_hash)
            bot.send_message(victim_chat_id, transaction_message)
            bot.send_message(victim_chat_id, hack_message)


