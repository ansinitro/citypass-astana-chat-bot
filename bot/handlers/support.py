from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import LOG_CHANNEL
from handlers.database import DB

async def forward_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button_text = update.message.text
    user_id = update.message.from_user.id


    if button_text == "Билеты":
        await update.message.reply_text(update.message)
        return
    
    document = await DB.col.find_one({'id': update.message.from_user.id})
    if not (document and document.get('forward', False)):
        return
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Stop", callback_data=f'/stop {user_id}'), 
                                         InlineKeyboardButton(text="Start", callback_data=f'/start {user_id}')],])
    await context.bot.send_message(LOG_CHANNEL,
                                f"{user_id} {button_text}",reply_markup=reply_markup)
    await update.message.reply_text("Ожидайте пока вам ответят наши админы)")

async def forward_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = None
    try:
        user_id = int(update.channel_post.reply_to_message.text.split(' ')[0])
    except ValueError:
        user_id = None
    if user_id:
        await context.bot.send_message(
            chat_id=user_id,
            text=update.channel_post.text
        )
