import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from math import radians, sin, cos, sqrt, atan2
import json

try:
    with open('ratings.json', 'r') as file:
        ratings = json.load(file)
        print(ratings)
except FileNotFoundError:
    ratings = {}

bot = telebot.TeleBot('5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM')

landmarks = [
    {"name": "Эрмитаж", "address": "St. Petersburg, Дворцовая площадь 2", "description": "Описание Эрмитажа", "latitude": 59.9411, "longitude": 30.3156, 'link': 'https://towntravel.ru/interesnie-fakti-o-gorodah-rossyi/korotko-ob-ermitazhe.html'},
    {"name": "Петропавловская крепость", "address": "St. Petersburg, Peter and Paul Fortress", "description": "Описание Петропавловской крепости", "latitude": 59.9561, "longitude": 30.3161, 'link': 'https://wikiway.com/russia/sankt-peterburg/petropavlovskaya-krepost/'},
    {"name": "Иисакиевский собор", "address": "St. Petersburg, St. Isaac's Square", "description": "Описание Иссакиевского собора", "latitude": 59.9343, "longitude": 30.3066, 'link': 'https://cathedral.ru/ru/isaac/building'},
]
users_data = {}
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, "Привет! Для начала поиска отправьте своё местоположение.", reply_markup=get_location_keyboard())

def get_location_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button)
    return keyboard

@bot.message_handler(content_types=['location'])
def handle_location(message):
    user_id = message.from_user.id
    global location
    location = message.location
    users_data[user_id] = {"location": location, "landmarks_sorted": None, "current_landmark_index": 0}
    sort_landmarks(user_id)

def sort_landmarks(user_id):
    users_data[user_id]["landmarks_sorted"] = sorted(landmarks, key=lambda x: calculate_distance(users_data[user_id]["location"].latitude, users_data[user_id]["location"].longitude, x["latitude"], x["longitude"]))
    send_landmark(user_id)

def send_landmark(user_id):
    if user_id not in users_data:
        return

    current_landmark_index = users_data[user_id]["current_landmark_index"]
    sorted_landmarks = users_data[user_id]["landmarks_sorted"]

    if current_landmark_index < len(sorted_landmarks):
        landmark = sorted_landmarks[current_landmark_index]

        distance_km = calculate_distance(
            users_data[user_id]["location"].latitude,
            users_data[user_id]["location"].longitude,
            landmark["latitude"],
            landmark["longitude"]
        )

        markup = get_landmark_keyboard()
        global last_message
        last_message = bot.send_photo(user_id, open(f"C:/Users/razuv/PycharmProjects/SPBHistoryBot/info/{landmark['name']}/{landmark['name']}.jpg", "rb"), caption=f"{landmark['name']} с оценкой: {get_ratings(landmark['name'])}\n{landmark['address']}\nРасстояние: {distance_km:.2f} км", reply_markup=markup)


    else:
        bot.send_message(user_id, "Больше нет ближайших мест.")

def get_landmark_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("Иду", callback_data="go"))
    markup.row(InlineKeyboardButton("Дальше", callback_data="next"))
    markup.row(InlineKeyboardButton("Закончить поиск", callback_data="finish"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    #print(call)
    if "last_message" in globals() and last_message.photo:
        bot.delete_message(call.message.chat.id, last_message.message_id)

    if call.data == "go":
        global landmark
        current_landmark_index = users_data[user_id]["current_landmark_index"]
        landmark = users_data[user_id]["landmarks_sorted"][current_landmark_index]
        bot.send_photo(user_id, open(f"C:/Users/razuv/PycharmProjects/SPBHistoryBot/info/{landmark['name']}/{landmark['name']}.jpg", "rb"))

        file_path = f"C:/Users/razuv/PycharmProjects/SPBHistoryBot/info/{landmark['name']}/{landmark['name']}.txt"

        # Открываем файл на чтение и считываем его содержимое
        with open(file_path, 'r', encoding='utf-8') as file:
            description = file.read()

        # Теперь переменная 'description' содержит текст из файла
        print(description)

        bot.send_message(user_id, f"{description}\n\nПодробнее: {landmark['link']}\n\nПожалуйста, оцените это место, если побывали там, или воздержитесь, если не смогли: /rate_place")
        #users_data[user_id]["current_landmark_index"] += 1
        #send_landmark(user_id)

    elif call.data == "next":
        users_data[user_id]["current_landmark_index"] += 1
        send_landmark(user_id)

    elif call.data == "finish":
        bot.send_message(user_id, "Поиск завершен.")
        users_data.pop(user_id, None)

@bot.message_handler(commands=['rate_place'])
def rate_place(message):
    markup = create_rating_keyboard()
    bot.send_message(message.chat.id, f"Ваша оценка для {landmark['name']}", reply_markup=markup)

def create_rating_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(str(i)) for i in range(1, 6)]
    buttons.append(KeyboardButton("Воздержусь от оценки"))
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['get_ratings'])
def get_ratings(message):
    bot.send_message(message.chat.id, text=f'{ratings}')
    print(1)

@bot.message_handler(func=lambda message: True)
def handle_rating(message):
    if message.text.isdigit() and 1 <= int(message.text) <= 5:
        # Обрабатываем выбор пользователем оценки
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, f"Спасибо за вашу оценку: {message.text}", reply_markup=markup)
        bot.send_message(-4031826999, text=f'Пользователь @{message.from_user.username} оценил {landmark["name"]} в {message.text} баллов.')
        if landmark['name'] in ratings:
            ratings[landmark['name']].append(message.text)
        else:
            # Если места нет в словаре, создаем новую запись
            ratings[landmark['name']] = [message.text]
        with open('ratings.json', 'w') as file:
            json.dump(ratings, file)
        print('JSON DUMP')
    elif message.text == "Воздержусь от оценки":
        # Обрабатываем выбор пользователем воздержаться от оценки
        bot.send_message(message.chat.id, "Вы воздержались от оценки.")
    else:
        #bot.send_message(message.chat.id, "Пожалуйста, используйте клавиатуру для оценки места.")
        pass


def get_ratings(place):
    if place in ratings:
        rating_list = ratings[place]
        rating = 0
        for i in rating_list:
            rating += int(i)
        rating /= len(rating_list)
        return rating
    else:
        return 'Ещё не оценивали'



def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Радиус Земли в км
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    a = sin(d_lat / 2) * sin(d_lat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(d_lon / 2) * sin(d_lon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  # Расстояние в км
    return distance

def yandexmap_detecting(place_long, place_lat):
    print(location)
    long1 = location.longtitude
    lat1 = location.latitude
    print(
        f'https://yandex.ru/maps/2/saint-petersburg/?ll={users_data.userid}%2C{lat1}&mode=routes&rtext={place_long}%2C{place_lat}~59.908411%2C30.318756&rtt=auto')

@bot.message_handler()
def send_text(message):
    bot.send_message(message.chat.id, 'command not found: maybe /start ?')

if __name__ == "__main__":
    bot.polling(none_stop=True)