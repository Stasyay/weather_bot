import requests
import config
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bot import *
from datetime import datetime

def get_wind_direction(deg):
    l = ['северный ','северо-восточный',' восточный','юго-восточный','южный ','юго-западный',' западный','северо-западный']
    for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res

# Проверка наличия в базе информации о нужном населенном пункте
def get_city_id(city):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': city, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': config.WEATHER_API_KEY})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        city_id = data['list'][0]['id']
    except Exception:
        pass
    assert isinstance(city_id, int)
    return city_id

# Запрос текущей погоды
def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': config.WEATHER_API_KEY})
        data = res.json()
        # print("data:", data)

        weather_answer = str(f'''сейчас в городе {data['name']} {data['weather'][0]['description']} 
температура  {data['main']['temp']} \nощущается как  {data['main']['feels_like']}
ветер {get_wind_direction(data['wind']['deg'])} {data['wind']['speed']} м/с 
рассвет {datetime.fromtimestamp(data['sys']['sunrise'])} \nзакат {datetime.fromtimestamp(data['sys']['sunset']) }''')
          
    except Exception: 
        pass
    return weather_answer

