from config import LOG_CHANNEL, BOT_TOKEN

from telegram import Update
from telegram.ext import ContextTypes

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(LOG_CHANNEL, update.message.location)