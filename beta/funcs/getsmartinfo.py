import wikipedia
from googletrans import Translator

def takesmartinfo(place):
    place_name = place
    exc = None
    translator = Translator()
    try:
        page = wikipedia.page(place_name)
        name = page.title
        description = translator.translate(page.summary, dest='ru')
        link = page.url
        img = page.images[0]
        return name, description.text, link, img, exc
    except:
        exc = "Ошибка поиска Wikipedia API :("
        name = None,
        description = None,
        link = 0
        img = 0
        return name, description, link, img, exc


#print(takesmartinfo('Собор Исаакия Далматского'))