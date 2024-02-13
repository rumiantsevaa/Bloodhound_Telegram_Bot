# Импорт всего для взаимодействия с тг
import requests
from config import SERPAPI_KEY

# Команда /yandexbhsearch


# Функция perform_yandex_reverse_image_search
def perform_yandex_reverse_image_search(photo_url):
    base_url = 'https://serpapi.com/search'
    params = {
        'engine': 'yandex_images',
        'url': photo_url,
        'api_key': SERPAPI_KEY,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'image_results' in data:
        search_results = [result.get('link', result.get('source')) for result in data['image_results']]

        return search_results
    else:
        return ["Извините, не удалось выполнить поиск по изображению."]
