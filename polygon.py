import telebot
from telebot import types
from geopy.geocoders import Nominatim
from math import radians, sin, cos, sqrt, atan2
from urllib.request import urlopen
import datetime

bot = telebot.TeleBot('5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM')
geolocator = Nominatim(user_agent="YOUR_APP_NAME")

class State:
    WAITING_FOR_LOCATION = 0
    WAITING_FOR_FEEDBACK = 1

state = State.WAITING_FOR_LOCATION
landmarks = [
    {"name": "Музей Эрмитаж", "address": "Санкт-Петербург, Дворцовая площадь 2"},
    {"name": "Петропавловская крепость", "address": "St. Petersburg, Peter and Paul Fortress"},
    {"name": "Иисаковский собор", "address": "St. Petersburg, St. Isaac's Square"},
]




sorted_landmarks = []
current_landmark_index = 0


def takeinfo(m):
    bot.send_message(m, "Старейший памятник архитектуры Санкт-Петербурга, крепость I класса. Расположена на Заячьем острове, в Санкт-Петербурге, историческое ядро города."
                        " Дата закладки крепости 27 мая 1703 года, является датой основания Санкт-Петербурга. Никогда не использовалась ни в одном сражении."
                        " С первой четверти XVIII века до начала 1920-х годов служила тюрьмой. С 1924 года является государственным музеем.",
                     reply_markup=get_next_keyboard())
    bot.send_photo(m, "https://photobuildings.com/photo/01/16/15/116154.jpg")
    bot.send_message(m, f'TODAY: {datetime.datetime.today().strftime("%A")}\n'
                        ""
                        "dГрафик работы сегодня: 10:00-18:30")
@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type == 'private':
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
        keyboard.add(button_geo)
        bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, text='Working only in local chats')

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
        for landmark in landmarks:
            location = geolocator.geocode(landmark["address"])
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

    button_next = telebot.types.KeyboardButton(text="Next")
    button_stop = telebot.types.KeyboardButton(text="Stop")
    keyboard.add(button_yes, button_next, button_stop)
    return keyboard

@bot.message_handler(func=lambda message: state == State.WAITING_FOR_FEEDBACK)
def handle_feedback(message):
    global state
    if message.text == "Иду":
        takeinfo(message.chat.id)
    elif message.text == "No":
        bot.send_message(message.chat.id, "We apologize. Do you want to see the next landmark?", reply_markup=get_next_keyboard())
        state = State.WAITING_FOR_FEEDBACK
    elif message.text == "Next":
        global current_landmark_index
        current_landmark_index += 1
        if current_landmark_index < len(sorted_landmarks):
            send_landmark_message(message.chat.id)
            state = State.WAITING_FOR_FEEDBACK
        else:
            bot.send_message(message.chat.id, "Вы просмотрели все места в вашем радиусе.", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
            state = State.WAITING_FOR_LOCATION
    elif message.text == "Stop":
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

bot.polling(none_stop=True, interval=0)