# -*- coding: utf-8 -*-
from string import Template

### Службові налаштування ###
BOT_TOKEN = "" # Токен бота. Необхідно вказати для роботи
DATABASE_FILE = "bot_base.db" # Адреса бази даних. Не змінюйте, якщо не певні у тому, що робите!
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S" # Формат виведення дати та часу.
HACKING_ALLOWED = True # Вказує, чи активний додатковий модуль "хакінгу". Вкажіть True для ввімкнення, False для вимкнення
DEFAULT_FINANCES = 1000

### Налаштування текстів службових повідомлень ###
WELCOME_MESSAGE = "Вітаю! Я - LARP Banking Bot, перший неспецифічний бот для банкінгу у рольових іграх живої дії на базі платформи Telegram; введіть /help для інструкцій"
HELP_MESSAGE = """
Дужки вказані для виділення; у команді потрібно вказувати значення без дужок
Загальні команди:
/start - прочитати привітання
/help - довідка/список загальних команд
/admin_help - довідка/список адміністративних команд
/hacker_help -  довідка/список хакерських команд
/register [ім'я персонажа] - реєстрація персонажа (1 персонаж на 1 користувача на 1 гру)
/inspect - дані про персонажа (якщо його зареєстровано)
/message [хеш персонажа] [текст повідомлення] - передати повідомлення через бота (підписане хешем вашого персонажа)
/history_sent - вивести список надісланих транзакцій 
/history_recieved - вивести список отриманих транзакцій
/history_all - вивести список усіх власних транзакцій
/history_pair [хеш персонажа] - вивести список усіх транзакцій між вашим персонажем та ціллю
/send [хеш персонажа] [сума] - надіслати вказану суму персонажу з вказаним хешем з рахунку свого персонажа
/history_messages - вивести список усіх власних повідомлень
/history_messages_sent - вивести список надісланих повідомлень 
/history_messages_recieved - вивести список отриманих повідомлень
/history_messages_pair [хеш персонажа] - вивести список усіх повідомлень між вашим персонажем та ціллю
/add_contact [хеш персонажа] [ім'я персонажа] - додати у список контаків персонажа персонажа з вказаним хешем (під вказаним ім'ям)
/delete_contact [хеш персонажа] - видалити обраний хеш зі списку контактів
/contact_list - вивести список контактів персонажа

"""
ADMIN_HELP_MESSAGE = """
Дужки вказані для виділення; у команді потрібно вказувати значення без дужок
/create_admin - створення адміністративного користувача (якщо його ще не існує)
/delete [хеш персонажа] - видалення персонажа
/admin_hail [повідомлення] - надіслати адміністративне повідомлення усім зареєєстрованим гравцям
/inspect_all - дані про всіх зареєстрованих персонажів гри
/set_attribute [хеш персонажа] [назву атрибуту; одне зі списку - finances|hacker_level|hacker_defence|is_admin] [нове значення атрибуту] - встановити атрибут персонажа рівним значенню
/admin_inspect_user [хеш персонажа] - отримайте дані про профіль вказаного персонажа
/admin_history_recieved [хеш персонажа] - вивести список отриманих транзакцій для обраного персонажа
/admin_history_sent [хеш персонажа] - вивести список надісланих транзакцій для обраного персонажа
/admin_history_all [хеш персонажа] - вивести список усіх транзакцій персонажа
/admin_history_pair [хеш персонажа 1] [хеш персонажа 2 ]- вивести список усіх транзакцій між парою персонажів
/admin_history_messages [хеш персонажа] - вивести список усіх повідомлень цілі
/admin_history_messages_sent [хеш персонажа] - вивести список надісланих повідомлень цілі
/admin_history_messages_recieved [хеш персонажа] - вивести список отриманих повідомлень цілі
/admin_history_messages_pair [хеш персонажа 1] [хеш персонажа 2] - вивести список усіх повідомлень між парою персонажів
/admin_add_contact [хеш персонажа 1][хеш персонажа 2] [ім'я персонажа] - додати у список контаків персонажа 1 персонажа 2 з вказаним хешем (під вказаним ім'ям)
/admin_delete_contact [хеш персонажа 1] [хеш персонажа 2] - видалити обраний хеш зі списку контактів персонажа 1
/admin_contact_list [хеш персонажа] - вивести список контактів персонажа
"""
HACKER_HELP_MESSAGE = """
Дужки вказані для виділення; у команді потрібно вказувати значення без дужок
УСІ хакерські команди, якщо рівень хакерських здібностей ВАШОГО персонажа рівний за рівень захисту цілі, ПОВІДОМЛЯТЬ ціль про злам/повідомлення, і не спрацюють взагалі, якщо ціль краще захищена.
/h@ck_user [хеш персонажа] - отримайте дані про профіль вказаного персонажа
/h@ck_history_recieved [хеш персонажа] - вивести список отриманих транзакцій для обраного персонажа
/h@ck_history_sent [хеш персонажа] - вивести список надісланих транзакцій для обраного персонажа
/h@ck_history_all [хеш персонажа] - вивести список усіх транзакцій персонажа
/h@ck_history_pair [хеш персонажа 1] [хеш персонажа 2 ]- вивести список усіх транзакцій між парою персонажів
/h@ck_history_messages [хеш персонажа] - вивести список усіх повідомлень цілі
/h@ck_history_messages_sent [хеш персонажа] - вивести список надісланих повідомлень цілі
/h@ck_history_messages_recieved [хеш персонажа] - вивести список отриманих повідомлень цілі
/h@ck_history_messages_pair [хеш персонажа 1] [хеш персонажа 2] - вивести список усіх повідомлень між парою персонажів
"""

### Налаштування текстів помилок та повідомлень про заборону ###
NO_USER_ERROR = "Персонажа з таким хешем не знайдено у базі даних"
NO_ADMIN_ERROR = "Недостатній рівень доступу; потрібні повноваження адміністратора (майстра гри)"
ALREADY_ADMIN = "У цій базі даних уже зареєстровано адміністратора. Зверніться до адміністратора для підвищення рівня повноважень"
ADMIN_RECORD_CREATED = "Користувача-адміністратора створено. Ім'я персонажа: ADMIN, хеш персонажа: 0000000000"
ALREADY_REGISTERED = "У базі даних цієї гри уже зареєстровано персонажа на ваш юзернейм у Telegram. Введіть /inspect для деталей"
NO_NAME = "Необхідно вказати ім'я персонажа"
ATTRIBUTE_UPDATE_MESSAGE = "Значення обраного атрибуту оновлено"
TRANSACTION_NO_FINANCES = "Транзакцію не проведено: недостатньо фінансів на рахунку"
MESSAGE_SEND_RESULT = "Надіслано повідомлення:\n"
INCOMING_MESSAGE = "Надходить повідомлення:\n\n"
USER_DATA = "користувача"
SENT_TRANSACTIONS_DATA = "надіслані транзакції"
RECIEVED_TRANSACTIONS_DATA = "отримані транзакції"
NO_USERS_FOUND = "Немає даних про користувачів"
NO_USER_DATA = "Немає даних про персонажа"
NO_TRANSACTIONS_FOUND = "Немає транзакцій"
ATTRIBUTE_UPDATE_MESSAGE = "Вказаний атрибут персонажа оновлено"
ALREADY_HAVE_USER = "Персонажа з таким ім'ям уже зареєєстровано"
MESSAGE_SENDER = "\nВід:"
ZERO_TRANSACTION = "Транзакцію не проведено: неможливо провести нульову або від'ємну транзакцію"
SELF_TRANSACTION = "Транзакцію не проведено: неможливо провести транзакцію самому собі"
ADMIN_HAIL_PREFIX = "ПОВІДОМЛЕННЯ АДМІНІСТРАЦІЇ:"
HACKER_TOO_PROTECTED = "Недостатній рівень хакерських навичок."
TRANSACTIONS_DATA_HISTORY = "транзакції загалом"
NO_HACKING_ALLOWED_ERROR = "Для цієї гри підсистема хакінгу недоступна"
NO_MESSAGES_FOUND = "Немає повідомлень"
NO_ADDRESS_RECORDS = "Немає записів у книзі контактів"
NO_SELF_MESSAGING = ""
NO_SELF_ADDRESSING = ""
NO_DUPLICATES = ""
ADDRESS_RECORD_ADDED = ""
ADDRESS_RECORD_DELETION_MESSAGE = ""
SENT_MESSAGES_DATA = ""
MESSAGES_DATA_HISTORY = ""
RECIEVED_MESSAGES_DATA = ""

### Налаштування текстів з динамічно генерованими даними. НЕ ЗМІНЮЙТЕ змінні виду $name ###
REGISTRATION_MESSAGE = Template("Вашого персонажа зареєстровано. Ім'я персонажа: $character_name; хеш персонажа: $character_hash")
DELETION_MESSAGE = Template("Персонажа с хешем $character_hash було видалено")
TRANSACTION_MESSAGE = Template("Транзакцію підтверджено; від $sender_hash до $reciever_hash, на суму: $amount; хеш транзакції: $transaction_hash")
HACK_ALERT = Template("ПОПЕРЕДЖЕННЯ! Ваші дані про $data_type потрапили у руки до $hacker_hash")
if HACKING_ALLOWED:
    USER_MODEL_DATA = Template(
        "Ім'я персонажа: $character_name;\nХеш персонажа: $character_hash;\nДоступні фінанси: $finances;\nРівень хакерських здібностей: $hack_level;\nРівень захисту від зламу: $defence_level;\nСтворено: $created"
    )
else:
    USER_MODEL_DATA = Template(
        "Ім'я персонажа: $character_name;\nХеш персонажа: $character_hash;\nДоступні фінанси: $finances;\nСтворено: $created"
    )
TRANSACTION_MODEL_DATA = Template(
    "Хеш транзакції: $transaction_hash;\nсума транзакції: $amount;\nчас створення транзакції: $created;\nнадіслано від $sender_hash => $reciever_hash"
)
MESSAGE_MODEL_DATA = Template("[$created] $sender_hash -> $reciever_hash: $message_text")
ADDRESS_RECORD_DATA = Template("Запис з адресної книги $owner_hash: $target_name - $target_hash")
TRANSACTION_UNALLOWED_VALUE = Template("Неприпустиме значення транзакції: $value")
TRANSACTION_PAIR = Template("транзакції між вами та $second_user")
MESSAGES_PAIR = Template("повідомлення між вами та $second_user")
