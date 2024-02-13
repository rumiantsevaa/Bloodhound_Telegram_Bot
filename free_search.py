# Импорт всего для взаимодействия с тг
import requests
from config import PIXABAY_API_KEY

# Импорт ROYALTY FREE IMAGES
from pixabay.image import image

# Создаем объект Image с испоSERPAPI_KEYльзованием ключа Pixabay API
image_api = image(PIXABAY_API_KEY)


# Команда /freebhsearch
def perform_pixabay_search(query):
    base_url = 'https://pixabay.com/api/'
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'image_type': 'photo',  # You can adjust parameters based on your requirements
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'hits' in data:
        photo_urls = [hit['webformatURL'] for hit in data['hits']]
        return photo_urls
    else:
        return ["Извините, не удалось найти изображения."]
