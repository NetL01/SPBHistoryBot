import schedule
from datetime import datetime
import telebot
from yaweather import Russia, YaWeather
import random
import time
import sys


def main():
    print('check')

main()
# Main token to start
bot = telebot.TeleBot('5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM')
bot.send_message(-1001803296788, text=f"{datetime.now()} bot started")
# bot.send_message(-1001803296788, text=f" ")

try:
    @bot.message_handler(commands=[""])
    def nothing(message):
        bot.reply_to(message, text=f"дурак?")
        time.sleep(2)
        bot.reply_to(message, text=f"( а если серьёзно, попробуй /help )")

    @bot.message_handler(commands=["кто_дурак?"])
    def whodumb(message):
        bot.reply_to(message, text='дима пыльноу дурак')

    @bot.message_handler(commands=["help"])
    def help(message):
        bot.reply_to(message, text=f'Тебе уже ничто не поможет, валенок')

    @bot.message_handler(commands=['check', 'status'])
    def check(message):
        bot.reply_to(message, text=f'Bot status: working, {message.from_user.username}!')


    @bot.message_handler(commands=['pogoda'])
    def pogoda(message):
        pass


    # TODO LIST TASKBOARD

    @bot.message_handler(commands=['stats'])
    def stats(message):
        pass




    #@bot.my_chat_member_handler()
    #def my_chat_m(message: bot.types.ChatMemberUpdated):
    #    new = message.new_chat_member
    #    allowlist = []
    #    if new.status == "member" and message.chat.id not in allowlist:
    #        bot.leave_chat(message.chat.id)



    # @bot.message_handler(commands='permission')
    # def permission(message):
    # perm_message = message.text.split(' ')
    # if message.from_user.username == 'netl01':
    # if perm_message[1] == 'list':
    # for key, value in permission_list.items():
    # bot.send_message(message.chat.id, text=f"{key}")
    # if perm_message[1] == 'add':
    # permission_list[perm_message[2]] = 0
    # bot.reply_to(message.chat.id, text=f"saved.")
    # if perm_message[1] == 'del':
    # if perm_message[2] in permission_list:
    # del permission_list[perm_message[2]]
    # bot.reply_to(message.chat.id, text=f"deleted.")
    # else:
    # bot.reply_to(message.chat.id, text=f"not found")
    # else:
    # bot.reply_to(message, text=f"Permission deny")

    @bot.message_handler(commands=['stop'])
    def exit(message):
        if message.from_user.username == "netl01":
            bot.reply_to(message, text=f"Bot stopped.")
            crashlist = [1, 2, 3]
            for i in range(len(crashlist) + 10):
                a = crashlist[i]
        else:
            bot.reply_to(message, text=f'Permission deny.')


    bot.polling(none_stop=True, interval=0)



except:
    print('crashed')
    # bot.send_message(-1001803296788, text=f"{datetime.now()} bot was stopped!")



    #thr.is_alive()  # Will return whether foo is running currently

    #thr.join()  # Will wait till "foo" is done