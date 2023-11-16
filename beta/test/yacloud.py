
import telebot

bot = telebot.TeleBot("5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM")

bot.remove_webhook()
bot.set_webhook("https://d5d7i1u52thov9hv65b0.apigw.yandexcloud.net")
bot.delete_webhook()