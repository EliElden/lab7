import os
import json
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# ==========================================
# КОНСТАНТЫ
# ==========================================
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
ASTROS_API_URL = 'http://api.open-notify.org/astros.json'
OUTPUT_JSON_FILE = 'variant_10.json'


def get_weather(city_name: str) -> None:
    """
    Получает и выводит текущую погоду для указанного города 
    через API OpenWeatherMap.
    
    :param city_name: Название города (например, 'Moscow').
    """
    if not WEATHER_API_KEY:
        print("Ошибка: Ключ API (WEATHER_API_KEY) не найден в .env файле.\n")
        return

    # Передаем параметры через словарь, чтобы не клеить длинную строку URL
    params = {
        'q': city_name,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    
    try:
        response = requests.get(WEATHER_API_BASE_URL, params=params)
        data = response.json()
        
        if data.get('cod') == 200:
            print(f'\n--- Погода в городе {city_name} ---')
            print(f'1. Описание: {data["weather"][0]["description"].capitalize()}')
            print(f'2. Температура: {data["main"]["temp"]} °C')
            print(f'3. Ощущается как: {data["main"]["feels_like"]} °C')
            print(f'4. Влажность: {data["main"]["humidity"]}%')
            print(f'5. Давление: {data["main"]["pressure"]} гПа')
            print('-----------------------------------\n')
        else:
            error_msg = data.get("message", "Город не найден или ошибка API.")
            print(f'Ошибка: {error_msg}\n')
            
    except requests.exceptions.RequestException as e:
        print(f'Проблема с подключением: {e}\n')


def get_space_info() -> None:
    """
    Запрашивает список людей, находящихся в космосе в данный момент, 
    выводит их на экран и сохраняет ответ сервера в JSON-файл.
    """
    try:
        response = requests.get(ASTROS_API_URL)
        data = response.json()

        if data.get('message') == 'success':
            with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
                
            print(f'✅ Ответ сервера успешно сохранен в \'{OUTPUT_JSON_FILE}\'')

            print('\n--- Люди в космосе прямо сейчас ---')
            print(f'Всего людей: {data.get("number", 0)}')
            
            for i, person in enumerate(data.get('people', []), 1):
                # Используем двойные кавычки снаружи, чтобы внутри можно было обратиться по ключу ['name']
                print(f"Космонавт {i} -> Имя: {person['name']} | Корабль: {person['craft']}")
            print('-----------------------------------\n')
        else:
            print('Ошибка при получении данных о космонавтах.\n')
            
    except requests.exceptions.RequestException as e:
        print(f'Проблема с подключением: {e}\n')


if __name__ == '__main__':
    while True:
        print('1 - Узнать погоду (OpenWeatherMap)')
        print('2 - Кто в космосе? (Вариант 10)')
        print('0 - Выход')
        
        choice = input('Выберите действие: ')
        
        match choice:
            case '1':
                city = input("Введите название города:\n(Подсказка: например, Moscow или Madrid)\n-> ")
                if city.strip():
                    get_weather(city)
                else:
                    print("Название города не может быть пустым!\n")
            case '2':
                get_space_info()
            case '0':
                print('Работа завершена.')
                break
            case _:
                print('Неверный ввод!\n')