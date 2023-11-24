import telebot
import geopy
from geopy.geocoders import Nominatim

token = '5849840132:AAEHFN1i-u6ZiglFRYL4jcwvL-1_R9DuKdM'
bot = telebot.TeleBot(token)
geolocator = Nominatim(user_agent="YOUR_APP_NAME")