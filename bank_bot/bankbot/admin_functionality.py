from bank_bot.bankbot.core import bot, client_factory
from bank_bot import settings
from bank_bot.banking_system import UserError, TransactionError, Database, HackerError, MessageError, AddressRecordError


@bot.message_handler(commands=['create_admin',])
def create_admin(message):
    # Admin creation command; works if user has no registered account in bot and no admins were created.
    client = client_factory.create_client(message)
    try:
        admin_creation_message = client.create_admin()
    except UserError as e:
        admin_creation_message = e.message
    bot.send_message(client.chat_id,admin_creation_message)

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
def admin_inspect_contact_list(message):
    client = client_factory.create_client(message)
    try:
        results = client.admin_inspect_contact_list(message.text)
    except (UserError, AddressRecordError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)


@bot.message_handler(
    func=lambda message: message.document is not None and message.document.mime_type == 'text/csv' and message.caption.startswith("/admin_mass_character_csv"),
    content_types=['document']
)
def admin_mass_set_character_csv(message):
    client = client_factory.create_client(message)
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        results = client.admin_mass_set_character_csv(downloaded_file)
    except UserError as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)

@bot.message_handler(
    func=lambda message: message.document is not None and message.document.mime_type == 'text/csv' and message.caption.startswith("/admin_mass_contact_csv"),
    content_types=['document']
)
def admin_mass_set_contact_csv(message):
    client = client_factory.create_client(message)
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        results = client.admin_mass_set_contact_csv(message.document)
    except (UserError, AddressRecordError,) as err:
        bot.send_message(client.chat_id, err.message)
        return
    bot.send_message(client.chat_id, results)
