import telebot
import geopy
from geopy.geocoders import Nominatim

bot = telebot.TeleBot('5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM')
geolocator = Nominatim(user_agent="YOUR_APP_NAME")

ChatIdRepo = {"Dima Borisov": 953910033, "Dima Pilnov": 0}
