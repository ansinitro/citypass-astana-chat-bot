import requests, json
from config import LOG_CHANNEL, BOT_TOKEN
from utils import utils

from telegram import Update, KeyboardButton,ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

async def callbackRecognize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    lang = query.from_user.language_code

    # update.message.from_user.language_code == 'en'
    if query.data == '/sight/<name>':
      response = requests.get(f'http://localhost:8000/sight/{context.user_data["last_searched_sight"]}')
      
      if response.status_code == 200:
        all_info = response.json()
        if lang == 'en':
          name, description, address, ticket_price, reach, show_map, buy_ticket, tour, no_info = 'Name', 'Description', 'Address', 'Ticket Price', 'Reach to', 'Show Map', 'Buy Tickets', '3D Tour', 'No Info'
        elif lang == 'kz':
          name, description, address, ticket_price, reach, show_map, buy_ticket, tour, no_info = "Аты", "Сипаттамасы", "Мекен-жайы", "Билет құны","Жету", "Картаны көрсету", "Билеттерді сатып алу", "3D-тур", 'Ақпарат Жоқ'
        else:
          name, description, address, ticket_price, reach, show_map, buy_ticket, tour, no_info = "Название", "Описание", "Адрес", "Стоимость билета", "Добраться до", "Показать карту", "Купить билеты", "3D-тур", 'Нет информации'

        replyKeyboardMarkup = ReplyKeyboardMarkup([[KeyboardButton(tour, web_app=WebAppInfo(url=all_info['3d_tour']))],
                                              [KeyboardButton(f"{reach} {query.message.text}", request_location=True)],
                                              [KeyboardButton(show_map, web_app=WebAppInfo(url=f'https://2gis.kz/astana/geo/{all_info["2gis_id"]}/{all_info["2gis_coord_f"]}%2C{all_info["2gis_coord_s"]}'))],
                                              [KeyboardButton(text=buy_ticket, web_app=WebAppInfo(url="https://astana.citypass.kz/ru/kupit-citypass/"))]], resize_keyboard=True)
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
        await context.bot.send_message(context._chat_id, f'{name}: {all_info[f"name_{lang}"]}\n\n{description}: {all_info[f"description_{lang}"]}\n\n{address}: {all_info[f"address_{lang}"]}\n\n{ticket_price}: {no_info if all_info["ticket_price"] is None else all_info["ticket_price"]}',
                                    reply_markup=replyKeyboardMarkup)