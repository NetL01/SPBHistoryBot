from telebot.async_telebot import AsyncTeleBot
import asyncio
import time

bot = AsyncTeleBot('5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM')
bot.send_message(-1001803296788, text="Status: {bot pool was deleted himself}.")


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Bot not here, here is ASYNCO KKH BOOOOOOOOTTT!!!.
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)

async def check_1():
    while True:
        time.sleep(1)
        print(1)

asyncio.run(check_1())
asyncio.run(bot.polling())
