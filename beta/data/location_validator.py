errors = []
import sys
from geopy.geocoders import Nominatim
from tqdm import tqdm
from colorama import Fore
from landmarks import landmarks
geolocator = Nominatim(user_agent="myapp")

def print_progress(index, total, message):
    progress = (index / total) * 100
    print(f"{Fore.YELLOW}{progress:.2f}% {message}")

with tqdm(total=len(landmarks), desc="Processing", unit="place", ncols=100) as pbar:
    for landmark in landmarks:
        location = geolocator.geocode(landmark["address"])
        if location is not None:
            pbar.update(1)
            print_progress(pbar.n, pbar.total, "Good")
        else:
            pbar.update(0)
            errors.append(landmark["name"])

print('\nFound results:')
if errors:
    print('Places there are not found:')
    for error in errors:
        print(error)
else:
    print('All places was found!')