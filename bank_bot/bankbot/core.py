import telebot
from telebot import util

from bank_bot.banking_system import BankingClientFactory, Database
from bank_bot import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)
database = Database(settings.DATABASE_FILE)
database.initialize_system()
client_factory = BankingClientFactory(database)

def safe_send_message(bot, chat_id, message):
    splitted_text = util.split_string(message, 4000)
    for text in splitted_text:
        bot.send_message(chat_id, text)
