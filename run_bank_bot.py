#!/usr/bin/env python
from bank_bot.bankbot import bot

if __name__ == "__main__":
    while True:
        bot.polling()
    print("TURN OFF")
