import random
from yamager import Yamager

def GetAnimeLittleGirl(query):
    yamager = Yamager()
    images = yamager.search_yandex_images(query)
    if images:
        previews = random.choice(images)
        return(yamager.get_best_image(previews))
    else:
        return None

