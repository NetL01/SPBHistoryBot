import wikipedia
import sys
from geopy.geocoders import Nominatim
from tqdm import tqdm
from colorama import Fore
from landmarks import landmarks
from art import tprint
geolocator = Nominatim(user_agent="myapp")


errors = []
badwikis = []
def print_progress(index, total, message):
    progress = (index / total) * 100
    print(f"{Fore.YELLOW}{progress:.2f}% {message}")

with tqdm(total=len(landmarks), desc="Processing", unit="place", ncols=100) as pbar:
    for landmark in landmarks:
        wikistatus = ''
        try:
            page = wikipedia.page(landmark["name"])
            wikistatus = 'Success'
        except wikipedia.exceptions.PageError:
            wikistatus = 'Wikipedia not found'
            badwikis.append(landmark["name"])
        location = geolocator.geocode(landmark["address"])
        if location is not None:
            pbar.update(1)
            print_progress(pbar.n, pbar.total, wikistatus)
        else:
            pbar.update(0)
            errors.append(landmark["name"])


print('-'*20)
print('-'*20)
print('-'*20)
tprint('FOUND RESULTS')
print('ERRORS:')
if errors:
    print('Places there are not found:')
    for error in errors:
        print(error)
else:
    print('All places was found!')
print('\n')
print('WIKI WARNINGS:')
if badwikis:
    print('Wiki~s where are not found:')
    for badwiki in badwikis:
        print(badwiki)
else:
    print('All wiki was found!')