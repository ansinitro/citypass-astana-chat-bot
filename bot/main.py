import json, os, requests
import logging, datetime

# config
from config import LOG_CHANNEL, BOT_TOKEN

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

#db
from handlers.database import Database
from handlers.location import location
from handlers.start import start
from handlers.messageHandler import messageHandler
from handlers.callbackRecognize import callbackRecognize
from handlers.photo import photo


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={update.message.photo[len(update.message.photo) - 1].file_id}')

    if response.ok:
        json_data = response.json()
        file_path = json_data.get('result').get('file_path')
    await context.bot.send_message(LOG_CHANNEL, f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}')


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    # application.add_handler(MessageHandler(filters.ALL, location))
    application.add_handler(MessageHandler(filters.LOCATION, location))
    application.add_handler(MessageHandler(filters.PHOTO, photo))
    application.add_handler(CallbackQueryHandler(callbackRecognize))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, messageHandler))

    # application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, forward_to_chat))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()