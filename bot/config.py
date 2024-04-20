import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    raise Exception("Please setup the .env variable TELEGRAM_TOKEN")

LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002063225065"))
AUTH_USERS = set(int(x) for x in os.getenv("AUTH_USERS").split())
DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))

