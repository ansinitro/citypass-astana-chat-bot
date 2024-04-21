from config import LOG_CHANNEL
from handlers.database import DB
import logging

from telegram import Update, KeyboardButton,ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    id = update.message.from_user.id
    
    if not await DB.is_user_exist(id):
        await DB.add_user(id)
        if LOG_CHANNEL:
            await context.bot.send_message(
                LOG_CHANNEL,
                f"#NewUser :- Name : {update.message.from_user.first_name} ID : {update.message.from_user.id}")
        else:
            logging.info(f"#NewUser :- Name : {update.message.from_user.first_name} ID : {update.from_user.id}")
            
    keyboard = [
        [KeyboardButton(text="Купить Билеты Citypass", web_app=WebAppInfo(url="https://astana.citypass.kz/ru/kupit-citypass/"))],
    ]
    
    await update.message.reply_text("hihihih", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
