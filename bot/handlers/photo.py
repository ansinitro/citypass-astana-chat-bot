import requests
from config import LOG_CHANNEL, BOT_TOKEN
from utils import utils

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

inline_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Получить Информацию", callback_data='/sight/<name>')]])


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={update.message.photo[0].file_id}')

    # Check if the request was successful (status code 200)
    if response.ok:
        json_data = response.json()
        file_path = json_data.get('result').get('file_path')
    city_name = utils.download_send_and_delete(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}', f"{context._user_id}.jpg", 'http://localhost:8000/recognize_image')
    await context.bot.send_message(context._chat_id, city_name, reply_markup=inline_keyboard)
