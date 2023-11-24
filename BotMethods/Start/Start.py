import telebot
from Configs.MainRequirements import bot

class Start:

    def __init__(self, bot, message):
        self.message = message
        self.bot = bot
        self.start(self.message)

    def start(self, message):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)
        self.bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            print('hello')


