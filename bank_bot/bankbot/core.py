import telebot

from bank_bot.banking_system import BankingClientFactory, Database
from bank_bot import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)
database = Database(settings.DATABASE_FILE)
database.initialize_system()
client_factory = BankingClientFactory(database)
