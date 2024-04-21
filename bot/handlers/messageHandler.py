from config import LOG_CHANNEL, BOT_TOKEN

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

import requests

async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE):
  response = requests.get('http://localhost:8000/recognize_input', json={"user_input" : update.message.text})
  if response.status_code == 200:
      print(response.json())
      suggested_input = response.json()['suggested_input']
      if suggested_input == None:
         await context.bot.send_message(context._chat_id, "Я вас не понял, ввидите свой запрос заново).")
         return
      context.user_data['last_searched_sight'] = suggested_input

      response = requests.get(f'http://localhost:8000/sight/{suggested_input}')
      if response.status_code == 200:
        all_info = response.json()
        replyKeyboardMarkup = ReplyKeyboardMarkup([[KeyboardButton("3D Тур", web_app=WebAppInfo(url=all_info['3d_tour']))],
                                              [KeyboardButton(f"Проехать до {suggested_input}", request_location=True)],
                                              [KeyboardButton("Показать на карте", web_app=WebAppInfo(url=f'https://2gis.kz/astana/geo/{all_info["2gis_id"]}/{all_info["2gis_coord_f"]}%2C{all_info["2gis_coord_s"]}'))],
                                              [KeyboardButton(text="Купить Билеты Citypass", web_app=WebAppInfo(url="https://astana.citypass.kz/ru/kupit-citypass/"))]], resize_keyboard=True)
        await context.bot.send_message(context._chat_id, f'Название: {all_info["name_ru"]}\n\nОписание: {all_info["description_ru"]}\n\nАддресс: {all_info["address"]}\n\nЦена за билет: {"Нет информаций" if all_info["ticket_price"] is None else all_info["ticket_price"]}',
                                 reply_markup=replyKeyboardMarkup)