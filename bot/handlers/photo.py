import requests
from config import LOG_CHANNEL, BOT_TOKEN

from telegram import Update
from telegram.ext import ContextTypes

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={update.message.photo[0].file_id}')

    # Check if the request was successful (status code 200)
    if response.ok:
        json_data = response.json()
        file_path = json_data.get('result').get('file_path')

    await context.bot.send_message(LOG_CHANNEL, f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}')
