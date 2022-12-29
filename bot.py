from telegram import Update
from telegram.ext import Updater, CommandHandler, ContextTypes
from owm_request import *

async def start_command(update: Update, context: ContextTypes):
    await update.message.reply_text(f'Привет {update.effective_user.first_name}! Могу рассказать о погоде')
    await start_getting_city(update, context)

async def start_getting_city(update: Update, context: ContextTypes):
    await update.message.reply_text(f' Погоду в каком городе ты хочешь узнать?')
 
def text (update: Update, context: ContextTypes):
    return received_city(update, context)

async def received_city(update: Update, context: ContextTypes):
    try:
        city = str(update.message.text)
        context.user_data['city'] = city
        # get_city_id(city)
        # request_current_weather(get_city_id(city))
        answer = request_current_weather(get_city_id(city))
    except:
        answer = 'Не могу найти такой город'

    await update.message.reply_text(answer)