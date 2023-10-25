from datetime import datetime
import telebot
from telebot import types
import time
from gmplot import gmplot
from math import radians, sin, cos, sqrt, atan2
from geopy.geocoders import Nominatim

# Main token to start
bot = telebot.TeleBot('5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM')
bot.send_message(-4031826999, text=f"{datetime.now()} bot started")
# bot.send_message(-1001803296788, text=f" ")
geolocator = Nominatim(user_agent="YOUR_APP_NAME")


try:
    # ADMINISTRATOR FUNCTIONS
    @bot.message_handler(commands=['check', 'status'])
    def check(message):
        print(message.chat.id)
        bot.reply_to(message, text=f'Bot status: working, {message.from_user.username}!')

    @bot.message_handler(commands=['stop'])
    def stop(message):
        if message.from_user.username == "netl01":
            # bot.reply_to(message, text=f"Bot stopped.")
            crashlist = [1, 2, 3]
            for i in range(len(crashlist) + 10):
                a = crashlist[i]
        else:
            bot.reply_to(message, text=f'Permission deny.')
    # GROUP CHAT FUNCTIONS


    # LOCAL CHAT FUNCTIONS
    @bot.message_handler(commands=["start"])
    def start(message):
        if message.chat.type == 'private':
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
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
            landmarks = [
                {"name": "Hermitage Museum", "address": "St. Petersburg, Palace Square, 2"},
                {"name": "Peter and Paul Fortress", "address": "St. Petersburg, Peter and Paul Fortress"},
                {"name": "St. Isaac's Cathedral", "address": "St. Petersburg, St. Isaac's Square"},
                # Add more landmarks here
            ]
            distances = []
            for landmark in landmarks:
                location = geolocator.geocode(landmark["address"])
                landmark_latitude = location.latitude
                landmark_longitude = location.longitude
                d = distance(latitude, longitude, landmark_latitude, landmark_longitude)
                distances.append({"name": landmark["name"], "distance": d})
            closest_landmark = sorted(distances, key=lambda x: x["distance"])[0]

            # Send message to user
            bot.send_message(message.chat.id,
                             f"The closest cultural landmark is {closest_landmark['name']} at {landmark['address']}.")


    def distance(lat1, lon1, lat2, lon2):
        R = 6371  # Radius of the earth in km
        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        a = sin(dLat / 2) * sin(dLat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dLon / 2) * sin(dLon / 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c  # Distance in km
        return distance


    bot.polling(none_stop=True, interval=0)


except:
    bot.send_message(-4031826999, text="bot inactive")
    print('crashed')