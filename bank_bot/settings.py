# -*- coding: utf-8 -*-
from string import Template
import configparser
import sys, os
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.split(os.path.abspath(__file__))[0])
my_config_parser = configparser.SafeConfigParser()
my_config_parser.read(application_path + '/config.cfg')

### Службові налаштування ###
BOT_TOKEN = my_config_parser.get("BOT_CONFIG", "BOT_TOKEN") # Токен бота. Необхідно вказати для роботи
DATABASE_FILE =  my_config_parser.get("BOT_CONFIG", "DATABASE_FILE") # Адреса бази даних. Не змінюйте, якщо не певні у тому, що робите!
DATETIME_FORMAT = my_config_parser.get("BOT_CONFIG", "DATETIME_FORMAT") # Формат виведення дати та часу.
HACKING_ALLOWED = my_config_parser.getboolean("BOT_CONFIG", "HACKING_ALLOWED") # Вказує, чи активний додатковий модуль "хакінгу". Вкажіть True для ввімкнення, False для вимкнення
DEFAULT_FINANCES = my_config_parser.getfloat("BOT_CONFIG", "DEFAULT_FINANCES")

### Налаштування текстів службових повідомлень ###
WELCOME_MESSAGE =  my_config_parser.get("BOT_HELP_WELCOME", "WELCOME_MESSAGE")
HELP_MESSAGE = my_config_parser.get("BOT_HELP_WELCOME", "HELP_MESSAGE")
ADMIN_HELP_MESSAGE = my_config_parser.get("BOT_HELP_WELCOME", "ADMIN_HELP_MESSAGE")
HACKER_HELP_MESSAGE = my_config_parser.get("BOT_HELP_WELCOME", "HACKER_HELP_MESSAGE")

### Налаштування текстів помилок та повідомлень про заборону ###
NO_USER_ERROR = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_USER_ERROR")
NO_ADMIN_ERROR = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_ADMIN_ERROR")
ALREADY_ADMIN = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ALREADY_ADMIN")
ADMIN_RECORD_CREATED = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ADMIN_RECORD_CREATED")
ALREADY_REGISTERED = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ALREADY_REGISTERED")
NO_NAME = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_NAME")
ATTRIBUTE_UPDATE_MESSAGE = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ATTRIBUTE_UPDATE_MESSAGE")
TRANSACTION_NO_FINANCES = my_config_parser.get("BOT_ERROR_NOTIFICATION", "TRANSACTION_NO_FINANCES")
MESSAGE_SEND_RESULT = my_config_parser.get("BOT_ERROR_NOTIFICATION", "MESSAGE_SEND_RESULT")
INCOMING_MESSAGE = my_config_parser.get("BOT_ERROR_NOTIFICATION", "INCOMING_MESSAGE")
USER_DATA = my_config_parser.get("BOT_ERROR_NOTIFICATION", "USER_DATA")
SENT_TRANSACTIONS_DATA = my_config_parser.get("BOT_ERROR_NOTIFICATION", "SENT_TRANSACTIONS_DATA")
RECIEVED_TRANSACTIONS_DATA = my_config_parser.get("BOT_ERROR_NOTIFICATION", "RECIEVED_TRANSACTIONS_DATA")
NO_USERS_FOUND = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_USERS_FOUND")
NO_USER_DATA = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_USER_DATA")
NO_TRANSACTIONS_FOUND = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_TRANSACTIONS_FOUND")
ATTRIBUTE_UPDATE_MESSAGE = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ATTRIBUTE_UPDATE_MESSAGE")
ALREADY_HAVE_USER = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ALREADY_HAVE_USER")
MESSAGE_SENDER = my_config_parser.get("BOT_ERROR_NOTIFICATION", "MESSAGE_SENDER")
ZERO_TRANSACTION = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ZERO_TRANSACTION")
SELF_TRANSACTION = my_config_parser.get("BOT_ERROR_NOTIFICATION", "SELF_TRANSACTION")
ADMIN_HAIL_PREFIX = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ADMIN_HAIL_PREFIX")
HACKER_TOO_PROTECTED = my_config_parser.get("BOT_ERROR_NOTIFICATION", "HACKER_TOO_PROTECTED")
TRANSACTIONS_DATA_HISTORY = my_config_parser.get("BOT_ERROR_NOTIFICATION", "TRANSACTIONS_DATA_HISTORY")
NO_HACKING_ALLOWED_ERROR = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_HACKING_ALLOWED_ERROR")
NO_MESSAGES_FOUND = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_MESSAGES_FOUND")
NO_ADDRESS_RECORDS = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_ADDRESS_RECORDS")
NO_SELF_MESSAGING = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_SELF_MESSAGING")
NO_SELF_ADDRESSING = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_SELF_ADDRESSING")
NO_DUPLICATES = my_config_parser.get("BOT_ERROR_NOTIFICATION", "NO_DUPLICATES")
ADDRESS_RECORD_ADDED = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ADDRESS_RECORD_ADDED")
ADDRESS_RECORD_DELETION_MESSAGE = my_config_parser.get("BOT_ERROR_NOTIFICATION", "ADDRESS_RECORD_DELETION_MESSAGE")
SENT_MESSAGES_DATA = my_config_parser.get("BOT_ERROR_NOTIFICATION", "SENT_MESSAGES_DATA")
MESSAGES_DATA_HISTORY = my_config_parser.get("BOT_ERROR_NOTIFICATION", "MESSAGES_DATA_HISTORY")
RECIEVED_MESSAGES_DATA = my_config_parser.get("BOT_ERROR_NOTIFICATION", "RECIEVED_MESSAGES_DATA")

### Налаштування текстів з динамічно генерованими даними. НЕ ЗМІНЮЙТЕ змінні виду $name ###
REGISTRATION_MESSAGE = Template(my_config_parser.get("BOT_TEMPLATE", "REGISTRATION_MESSAGE"))
DELETION_MESSAGE = Template(my_config_parser.get("BOT_TEMPLATE", "DELETION_MESSAGE"))
TRANSACTION_MESSAGE = Template(my_config_parser.get("BOT_TEMPLATE", "TRANSACTION_MESSAGE"))
HACK_ALERT = Template(my_config_parser.get("BOT_TEMPLATE", "HACK_ALERT"))
if HACKING_ALLOWED:
    USER_MODEL_DATA = Template(
        my_config_parser.get("BOT_TEMPLATE", "USER_MODEL_DATA_HACKING_ON")
    )
else:
    USER_MODEL_DATA = Template(
        my_config_parser.get("BOT_TEMPLATE", "USER_MODEL_DATA")
    )
TRANSACTION_MODEL_DATA = Template(
    my_config_parser.get("BOT_TEMPLATE", "TRANSACTION_MODEL_DATA")
)
MESSAGE_MODEL_DATA = Template(my_config_parser.get("BOT_TEMPLATE", "MESSAGE_MODEL_DATA"))
ADDRESS_RECORD_DATA = Template(my_config_parser.get("BOT_TEMPLATE", "ADDRESS_RECORD_DATA"))
TRANSACTION_UNALLOWED_VALUE = Template(my_config_parser.get("BOT_TEMPLATE", "TRANSACTION_UNALLOWED_VALUE"))
TRANSACTION_PAIR = Template(my_config_parser.get("BOT_TEMPLATE", "TRANSACTION_PAIR"))
MESSAGES_PAIR = Template(my_config_parser.get("BOT_TEMPLATE", "MESSAGES_PAIR"))
