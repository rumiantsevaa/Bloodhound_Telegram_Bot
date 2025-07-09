# Импорт всего для взаимодействия с тг
import requests
from config import SERPAPI_KEY

# Команда /ultimatebhsearch


# Изменяем функцию perform_google_reverse_image_search
def perform_google_reverse_image_search(photo_url):
    base_url = 'https://serpapi.com/search'
    params = {
        'engine': 'google_reverse_image',
        'image_url': photo_url,
        'api_key': SERPAPI_KEY,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'image_results' in data:
        search_results = [result.get('link', result.get('source')) for result in data['image_results'][:10]] # Capacity limitations for results
        
        # Добавляем заголовок перед результатами
        if search_results:
            search_results.insert(0, "♐️ Что удалось найти..[В случае отсутствия результатов обратитесь с другим запросом к этому типу поиска спустя истечение лимита.]")
        return search_results
    else:
        return ["Извините, не удалось выполнить поиск по изображению 😱"]
