import json
import logging, datetime
from handlers.database import DB

# config
from config import DB_URL, DB_NAME, LOG_CHANNEL

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

#db
from handlers.database import Database
from handlers.support import forward_to_chat, forward_to_user

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a `/start` command handler.
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
        [KeyboardButton(text="Buscar paraderos cercanos", request_location=True)],
        [KeyboardButton(text="citypass", web_app=WebAppInfo(url="https://astana.citypass.kz/ru/kupit-citypass/"))],
    ]
    
    await update.message.reply_text("⭐️ Наш приоритет дать возможность купить любую игровую валюту по лучшим ценам, а также предоставить вам скорейшее получение доната с гарантией безопасности вашего аккаунта 💫", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))


async def location(update, context):
    # search for bus stops near received location
    await context.bot.send_message(LOG_CHANNEL, update.message.location)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7017134946:AAGKaUnGw4Np_7ByLSo3fbznOSant2yNYAs").build()
    application.add_handler(MessageHandler(filters.LOCATION, location))
    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, forward_to_chat))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()