#!/usr/bin/env python
from bank_bot.bankbot import bot, client_factory
import time

if __name__ == "__main__":
    while True:
        try:
            bot.polling()
        except Exception as e:
            client = client_factory.create_client("")
            admin_list = client.get_admins()
            for admin in admin_list:
                bot.send_message(admin.chat_id, e)
            time.sleep(5)
            print(e)
            pass
