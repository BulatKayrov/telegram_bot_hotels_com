import telebot
import os
from dotenv import load_dotenv
from peewee import SqliteDatabase
from loguru import logger


load_dotenv()
TOKEN = os.getenv("TOKEN")
API_KEY_HOTELS_COM = os.getenv("API_KEY_HOTELS_COM")
bot = telebot.TeleBot(token=TOKEN)


BASE_DIR = os.path.dirname(os.path.abspath('python_basic_diploma'))
DB_PATH = os.path.join(BASE_DIR, "database.db")
db = SqliteDatabase(DB_PATH)


LOG_PATH = os.path.join(BASE_DIR, f"storage_log{os.sep}debug.log")
logger.add(LOG_PATH, format='{time} | {level} | {message}', level='DEBUG')


