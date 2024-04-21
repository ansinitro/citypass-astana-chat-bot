import requests
from config import LOG_CHANNEL, BOT_TOKEN
from utils import utils

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={update.message.photo[0].file_id}')
    lang = update.message.from_user.language_code
    if lang == 'en':
        get_info = 'Receive information'
    elif lang == 'kz':
        get_info = 'Ақпарат алу'
    else:
        get_info = 'Получить Информацию'
    
    # Check if the request was successful (status code 200)
    if response.ok:
        json_data = response.json()
        file_path = json_data.get('result').get('file_path')
    city_names = utils.download_send_and_delete(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}', f"{context._user_id}.jpg", 'http://localhost:8000/recognize_image')
    context.user_data['last_searched_sight'] = city_names['id']

    city_names = city_names['names']
    await context.bot.send_message(context._chat_id, city_names[f'name_{update.message.from_user.language_code}'], 
                                   reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(get_info, callback_data='/sight/<name>')]]))
