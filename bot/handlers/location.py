from config import LOG_CHANNEL, BOT_TOKEN

from telegram import Update
from telegram.ext import ContextTypes

import requests

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.post(url, files=files)

    if response.status_code == 200:
        response_json = response.json()
        city_name = response_json.get('city_name')
        print(f"Photo sent successfully. City name: {city_name}")
        return city_name
    else:
        print("Failed to send photo")
        return None
    await context.bot.send_message(LOG_CHANNEL, update.message.location)