import requests, json
from config import LOG_CHANNEL, BOT_TOKEN
from utils import utils

from telegram import Update, KeyboardButton,ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

async def callbackRecognize(update: Update, context: ContextTypes.DEFAULT_TYPE):
  query = update.callback_query
  # update.message.from_user.language_code == 'en'
  if query.data == '/sight/<name>':
    context.user_data['last_searched_sight'] = query.message.text
    response = requests.get(f'http://localhost:8000/sight/{query.message.text}')
    if response.status_code == 200:
      all_info = response.json()
      replyKeyboardMarkup = ReplyKeyboardMarkup([[KeyboardButton("3D Тур", web_app=WebAppInfo(url=all_info['3d_tour']))],
                                            [KeyboardButton(f"Проехать до {query.message.text}", request_location=True)],
                                            [KeyboardButton("Показать на карте", web_app=WebAppInfo(url=f'https://2gis.kz/astana/geo/{all_info["2gis_id"]}/{all_info["2gis_coord_f"]}%2C{all_info["2gis_coord_s"]}'))],
                                            [KeyboardButton(text="Купить Билеты Citypass", web_app=WebAppInfo(url="https://astana.citypass.kz/ru/kupit-citypass/"))]], resize_keyboard=True)
      await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
      await context.bot.send_message(context._chat_id, f'Название: {all_info["name_ru"]}\n\nОписание: {all_info["description_ru"]}\n\nАддресс: {all_info["address"]}\n\nЦена за билет: {"Нет информаций" if all_info["ticket_price"] is None else all_info["ticket_price"]}',
                                 reply_markup=replyKeyboardMarkup)