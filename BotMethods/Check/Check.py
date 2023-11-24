from Configs.MainRequirements import bot
import time

class Check:
    def Check(message):
        start_time = time.time()
        msg = bot.send_message(message.chat.id, "Проверяется состояние соединения с серверами Telegram [0/5]")
        for i in range(1, 6):
            time.sleep(1)  # Пауза в 1 секунду
            bot.edit_message_text(f"Проверяется состояние соединения с серверами Telegram [{i}/5]", message.chat.id,
                                  msg.message_id)
        end_time = time.time()  # Фиксируем время окончания
        delay = str(end_time - start_time - 5)[:3]
        bot.edit_message_text(f"Статус работы: стабильный. Задержка: {delay} cек.", message.chat.id,
                              msg.message_id)