#!/usr/bin/env python
from bank_bot.bankbot import bot
import time

if __name__ == "__main__":
    keyboard_interrupt = False
    while not keyboard_interrupt:
        try:
            bot.polling()
        except KeyboardInterrupt:
            keyboard_interrupt = True
        except Exception as e:
            time.sleep(2)
            print(e)
            pass
