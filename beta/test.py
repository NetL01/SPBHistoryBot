import telebot
import openai

# Установите свой ключ API от OpenAI
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Установите ваш токен от BotFather
bot = telebot.TeleBot('5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM')


# Обработчик команды /chat
@bot.message_handler(commands=['chat'])
def handle_chat_command(message):
    # Отправляем инструкцию по использованию команды
    bot.send_message(message.chat.id,
                     "Вы можете использовать команду /chat для общения с ChatGPT. Просто отправьте ваш вопрос или сообщение.")


# Обработчик всех входящих сообщений
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Проверяем, является ли сообщение командой /chat
    if message.text.startswith('/chat'):
        # Извлекаем текст сообщения после команды /chat
        user_input = message.text[6:].strip()

        # Отправляем запрос к ChatGPT
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_input,
            max_tokens=150
        )

        # Отправляем ответ пользователя
        bot.send_message(message.chat.id, response.choices[0].text.strip())
    else:
        # Если не команда /chat, отправляем стандартный ответ
        bot.send_message(message.chat.id, "Привет! Я бот. Чтобы поговорить с ChatGPT, используйте команду /chat.")


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)









'''
# /start FUNCTIONS // ONLY LOCAL MESSAGES

class State:
    WAITING_FOR_LOCATION = 0
    WAITING_FOR_FEEDBACK = 1

state = State.WAITING_FOR_LOCATION

sorted_landmarks = []
current_landmark_index = 0

def takeinfo(m):
    name, desc, link, img, exc = getsmartinfo.takesmartinfo(sorted_landmarks[current_landmark_index]["name"])
    if exc == None:
        print(sorted_landmarks[current_landmark_index])
        bot.send_photo(m, link)
        if len(desc) > 100:
            short_desc = desc[:100] + "..."
            keyboard = types.InlineKeyboardMarkup()
            button_full = types.InlineKeyboardButton(text="Читать полностью", callback_data=f"full_desc_{current_landmark_index}")
            keyboard.add(button_full)
            bot.send_message(m, text=f"{short_desc}", reply_markup=keyboard)
        else:
            bot.send_message(m, text=f"{desc}")

    else:
        bot.send_message(m, text=f'Exception: {exc}')

@bot.callback_query_handler(func=lambda call: call.data.startswith("full_desc_"))
def full_desc_handler(call):
    index = int(call.data.split("_")[2])
    name, desc, link, img, exc = getsmartinfo.takesmartinfo(sorted_landmarks[index]["name"])
    if exc == None:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{desc}")
    else:
        bot.send_message(call.message.chat.id, text=f'Exception: {exc}')

@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type == 'private':
        bot.send_message(-4031826999, text=f'Пользователь @{message.from_user.username} начал взаимодействие /start')
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, text='Работает только в локальном чате.')

@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location is not None:
        # Store latitude and longitude in variables
        latitude = message.location.latitude
        longitude = message.location.longitude

        # Calculate distance to landmarks
        global sorted_landmarks
        global current_landmark_index
        distances = []
        for landmark in landmarks.landmarks:
            location = config.geolocator.geocode(landmark["address"])
            landmark_latitude = location.latitude
            landmark_longitude = location.longitude
            d = distance(latitude, longitude, landmark_latitude, landmark_longitude)
            distances.append({"name": landmark["name"], "address": landmark["address"], "distance": d})
        sorted_landmarks = sorted(distances, key=lambda x: x["distance"])
        current_landmark_index = 0

        # Send message to user
        global state
        state = State.WAITING_FOR_FEEDBACK
        send_landmark_message(message.chat.id)

def send_landmark_message(chat_id):
    global sorted_landmarks
    global current_landmark_index
    landmark = sorted_landmarks[current_landmark_index]
    bot.send_message(chat_id, f"{landmark['distance']:.2f} км от Вас:  {landmark['name']} "
                              f"По адресу: {landmark['address']}. Нравится?", reply_markup=get_feedback_keyboard())

def get_feedback_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_yes = telebot.types.KeyboardButton(text="Иду")

    button_next = telebot.types.KeyboardButton(text="Далее")
    button_stop = telebot.types.KeyboardButton(text="Остановить поиск")
    keyboard.add(button_yes, button_next, button_stop)
    return keyboard

@bot.message_handler(func=lambda message: state == State.WAITING_FOR_FEEDBACK)
def handle_feedback(message):
    global state
    if message.text == "Иду":
        takeinfo(message.chat.id)
    elif message.text == "No":
        bot.send_message(message.chat.id, "pass", reply_markup=get_next_keyboard())
        state = State.WAITING_FOR_FEEDBACK
    elif message.text == "Далее":
        global current_landmark_index
        current_landmark_index += 1
        if current_landmark_index < len(sorted_landmarks):
            send_landmark_message(message.chat.id)
            state = State.WAITING_FOR_FEEDBACK
        else:
            bot.send_message(message.chat.id, "Вы просмотрели все места в вашем радиусе.", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
            state = State.WAITING_FOR_LOCATION
    elif message.text == "Остановить поиск":
        bot.send_message(message.chat.id, "Поиск прекращён.", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
        state = State.WAITING_FOR_LOCATION

def get_next_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_next = telebot.types.KeyboardButton(text="Next")
    button_stop = telebot.types.KeyboardButton(text="Stop")
    keyboard.add(button_next, button_stop)
    return keyboard

def distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    a = sin(dLat / 2) * sin(dLat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2) * sin(dLon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  # Distance in km
    return distance


# /start METHODS ENDED








# DIMA'S IDIOTS FUN METHODS
@bot.message_handler(content_types=["voice", "sticker", "video", "document", "photo", "text"])
def Wiretapping(message):
    bot.forward_message(chat_id=-4031826999, from_chat_id=message.chat.id, message_id=message.id)



'''





























bot.polling(none_stop=True, interval=0)