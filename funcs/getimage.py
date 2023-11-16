import requests
from bs4 import BeautifulSoup

def get_image_url(query):
    url = f"https://photobuildings.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    image_url = soup.find("img", class_="img-fluid")["src"]
    return image_url

# Example usage
query = "Эрмитаж"
image_url = get_image_url(query)
print(image_url)