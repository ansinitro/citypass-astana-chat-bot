from config import LOG_CHANNEL
from handlers.database import DB
import logging

from telegram import Update, KeyboardButton,ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = update.message.from_user.id
    lang = update.message.from_user.language_code
    if lang == 'en':
      buy_tickets = 'Buy Tickets'
      hello = 'Write down the name of the attraction or upload a photo, and I will help you set a route or show it on the map.'
    elif lang == 'kk':
      buy_tickets = 'Билеттерді сатып алу'
      hello = 'Көрікті орынның атын жазыңыз немесе фотосуретті жүктеңіз, мен сізге маршрут құруға көмектесемін немесе оны картада көрсетемін.'
    else:
      buy_tickets = 'Купить билеты'
      hello = 'Напиши название достопримечательности или загрузи фото, и я помогу тебе построить маршрут или покажу её на карте.'
    if not await DB.is_user_exist(id):
        await DB.add_user(id)
        if LOG_CHANNEL:
            await context.bot.send_message(
                LOG_CHANNEL,
                f"#NewUser :- Name : {update.message.from_user.first_name} ID : {update.message.from_user.id}")
        else:
            logging.info(f"#NewUser :- Name : {update.message.from_user.first_name} ID : {update.from_user.id}")
            
    keyboard = [
        [KeyboardButton(text=buy_tickets, web_app=WebAppInfo(url="https://astana.citypass.kz/ru/kupit-citypass/"))],
    ]
    
    await update.message.reply_text(hello, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
