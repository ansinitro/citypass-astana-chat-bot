import json, os, requests
import logging, datetime
from handlers.database import DB

# config
from config import DB_URL, DB_NAME, LOG_CHANNEL, BOT_TOKEN

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters

#db
from handlers.database import Database

from handlers.support import forward_to_chat, forward_to_user
from handlers.photo import photo

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
    
    await update.message.reply_text("hihihih", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

def download_file(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
        print("File downloaded successfully")
    else:
        print("Failed to download file")

def send_photo(url, photo_path):
    with open(photo_path, 'rb') as file:
        files = {'image': file}
        response = requests.post(url, files=files)
    try:
        json_data = response.json()
    except ValueError:
        json_data = response
        
    if response.status_code == 200:
        print("Photo sent successfully")
    else:
        print("Failed to send photo")
    return json_data



async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={update.message.photo[len(update.message.photo) - 1].file_id}')
    if response.ok:
        json_data = response.json()
        file_path = json_data.get('result').get('file_path')
        print(file_path)
        download_file(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}', "./1.jpg")

    message_data = send_photo('http://localhost:8000/recognize_image', './1.jpg')
    message_text = str(message_data)
    # await context.bot.send_message(LOG_CHANNEL, message_text)
    await update.message.reply_text(message_text)



def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.ALL, location))
    application.add_handler(MessageHandler(filters.LOCATION, location))
    application.add_handler(MessageHandler(filters.PHOTO, photo))
    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, forward_to_chat))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()