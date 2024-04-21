import requests, json
from config import LOG_CHANNEL, BOT_TOKEN
from utils import utils

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

async def callbackRecognize(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  # update.message.from_user.language_code == 'en'
  if query.data == '/sight/<name>':
    context.user_data['last_searched_sight'] = query.message.text
    response = requests.get(f'http://localhost:8000/sight/{query.message.text}')
    if response.status_code == 200:
      all_info = response.json()
      inline_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("3D Тур", web_app=WebAppInfo(url=all_info['3d_tour']))],
                                            [InlineKeyboardButton("Проехать", callback_data='/sight/route')],
                                            [InlineKeyboardButton("Показать на карте", web_app=WebAppInfo(url=f'https://2gis.kz/astana/geo/{all_info["2gis_id"]}/{all_info["2gis_coord_f"]}%2C{all_info["2gis_coord_s"]}'))]])
      await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
      await context.bot.send_message(context._chat_id, f'Название: {all_info["name_ru"]}\n\nОписание: {all_info["description_ru"]}\n\nАддресс: {all_info["address"]}\n\nЦена за билет: {"Нет информаций" if all_info["ticket_price"] is None else all_info["ticket_price"]}',
                                 reply_markup=inline_keyboard)
  # if query.data == 'sight/route':
  