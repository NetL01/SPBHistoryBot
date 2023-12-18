from urllib.parse import urlencode


def generate_yandex_maps_route_url(start_coords, end_coords):
    base_url = "https://yandex.ru/maps"
    params = {
        "ll": f"{start_coords[0]},{start_coords[1]}",
        "rtext": f"{end_coords[0]},{end_coords[1]}",
        "rtt": "auto",
    }
    route_url = f"{base_url}/?{urlencode(params)}"
    return route_url

# Пример использования
user_coords = (59.9411, 30.3156)  # Координаты пользователя
destination_coords = (59.9343, 30.3066)  # Координаты места

route_url = generate_yandex_maps_route_url(user_coords, destination_coords)
print("Отправьте пользователю следующую ссылку для просмотра маршрута:")
print(route_url)
long1 = 59.9411
lat1 = 30.3156
long2 = 59.9343
lat2 = 30.3066
print(f'https://yandex.ru/maps/2/saint-petersburg/?ll={long1}%2C{lat1}&mode=routes&rtext={long2}%2C{lat2}~59.908411%2C30.318756&rtt=auto')
