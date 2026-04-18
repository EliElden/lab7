import requests
import json 
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city_name):
    KEY = os.getenv('WEATHER_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={KEY}&units=metric&lang=ru'
    
    response = requests.get(url)
    data = response.json()
    
    if data.get('cod') == 200:
        print(f'\n--- Погода в городе {city_name} ---')
        print(f'1. Описание: {data["weather"][0]["description"].capitalize()}')
        print(f'2. Температура: {data["main"]["temp"]} °C')
        print(f'3. Ощущается как: {data["main"]["feels_like"]} °C')
        print(f'4. Влажность: {data["main"]["humidity"]}%"')
        print(f'5. Давление: {data["main"]["pressure"]} гПа')
        print('-----------------------------------\n')
    else:
        print('Город не найден или ошибка API.\n')

def get_space_info():
    url = 'http://api.open-notify.org/astros.json'
    
    response = requests.get(url)
    data = response.json()

    if data.get('message') == 'success':
        with open('variant_10.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            
        print('✅ Ответ сервера успешно сохранен \'variant_10.json\'')

        print('\n--- Люди в космосе прямо сейчас ---')
        print(f'Всего людей: {data["number"]}')
        
        for i, person in enumerate(data['people'], 1):
            print(f'Космонавт {i} -> Имя: {person['name']} | Корабль: {person['craft']}')
        print('-----------------------------------\n')
    else:
        print('Ошибка при получении данных.\n')

while True:
    print('1 - Узнать погоду (OpenWeatherMap)')
    print('2 - Кто в космосе? (Вариант 10)')
    print('0 - Выход')
    
    choice = input('Выберите действие: ')
    
    match choice:
        case '1':
            city = input("Введите название города:\n(Подсказка: например, Moscow или Madrid)\n-> ")
            get_weather(city)
        case '2':
            get_space_info()
        case '0':
            print('Работа завершена.')
            break
        case _:
            print('Неверный ввод!\n')