import telebot

import beta.stary_pizdec.BotMethods.Start.Start
from beta.stary_pizdec.Configs.MainRequirements import token, bot
from beta.stary_pizdec.BotMethods.Echo import Echo
from beta.stary_pizdec.BotMethods.Check import Check


class MyBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)


    def start(self):
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            beta.stary_pizdec.BotMethods.Start.Start.Start(bot, message)

        @self.bot.message_handler(commands=['echo'])
        def echo_message(message):
            text = message.text[6:]
            Echo.Echo.doing(message, message.text)

        @self.bot.message_handler(commands=['check'])
        def check_message(message):
            Check.Check.Check(message)

        #@self.bot.message_handler(content_types=['text'])
        #def echo_message(message):
        #    self.bot.send_message(message.chat.id, text='/start')




        self.bot.polling()

if __name__ == '__main__':
    bot = MyBot(token)
    bot.start()