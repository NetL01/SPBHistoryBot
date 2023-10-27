import telebot
import geopy
from geopy.geocoders import Nominatim

bot = telebot.TeleBot('5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM')
geolocator = Nominatim(user_agent="YOUR_APP_NAME")