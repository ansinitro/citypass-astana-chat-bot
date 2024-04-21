from config import LOG_CHANNEL, BOT_TOKEN

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

import requests

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    json_info = {
        'sight_name':context.user_data['last_searched_sight'],
        'longitude': update.message.location.longitude,
        'latitude' : update.message.location.latitude
    }
    response = requests.get('http://localhost:8000/sight/route', json=json_info)

    if response.status_code == 200:
        link = response.json()['2gis_route']
    print(context.user_data['last_searched_sight'], link)
    
    await context.bot.send_message(context._chat_id,
                                   f'Проехать до {context.user_data["last_searched_sight"]}',
                                   reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Проехать", web_app=WebAppInfo(url=link))]]))