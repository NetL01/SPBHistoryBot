from Configs.MainRequirements import bot

class Echo:
        def doing(message, text):
                bot.send_message(message.chat.id, message.text)
                print('echo doing')
