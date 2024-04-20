import datetime

from config import DB_URL, DB_NAME, LOG_CHANNEL
import logging

from handlers.database import Database
from telegram import Update

db = Database(DB_URL, DB_NAME)
