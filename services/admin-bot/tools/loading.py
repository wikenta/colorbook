from dotenv import load_dotenv
import logging, os

# Константы для переменных окружения
ENV = 'ENV'
ENV_FOLDER = '../config'
ENV_MAIN = 'main'
ENV_DEVELOP = 'develop'
ENV_ADMIN = 'admin'

TELEGRAM_ENV_FILE = f"{ENV_FOLDER}/telegram.{os.getenv(ENV, ENV_DEVELOP)}.env"
TELEGRAM_BOT_LOGIN = 'TELEGRAM_BOT_LOGIN'
TELEGRAM_BOT_ID = 'TELEGRAM_BOT_ID'
TELEGRAM_API_TOKEN = 'TELEGRAM_API_TOKEN'

DB_ENV_FILE = f"{ENV_FOLDER}/db.env"
DB_USER = 'DB_USER'
DB_PASSWORD = 'DB_PASSWORD'
DB_NAME = 'DB_NAME'
DB_HOST = 'DB_HOST'

CLOUDINARY_ENV_FILE = f"{ENV_FOLDER}/cloudinary.env"
CLOUDINARY_CLOUD_NAME = 'CLOUDINARY_CLOUD_NAME'
CLOUDINARY_API_KEY = 'CLOUDINARY_API_KEY'
CLOUDINARY_API_SECRET = 'CLOUDINARY_API_SECRET'

def load_environment():
    """
    Загружает переменные окружения из .env файлов.
    """
    load_dotenv(TELEGRAM_ENV_FILE)
    load_dotenv(DB_ENV_FILE)
    load_dotenv(CLOUDINARY_ENV_FILE)

    #logger = logging.getLogger(__name__)
    #env = os.getenv(ENV, ENV_DEVELOP)
    #logger.info(f"Environment variables: {env}")

    #logger.info(f"TELEGRAM_ENV_FILE: {TELEGRAM_ENV_FILE}")
    #logger.info(f"TELEGRAM_BOT_LOGIN: {os.getenv(TELEGRAM_BOT_LOGIN)}")
    #logger.info(f"TELEGRAM_BOT_ID: {os.getenv(TELEGRAM_BOT_ID)}")
    #logger.info(f"TELEGRAM_API_TOKEN: {os.getenv(TELEGRAM_API_TOKEN)}")

    #logger.info(f"DB_ENV_FILE: {DB_ENV_FILE}")
    #logger.info(f"DB_USER: {os.getenv(DB_USER)}")
    #logger.info(f"DB_PASSWORD: {os.getenv(DB_PASSWORD)}")
    #logger.info(f"DB_NAME: {os.getenv(DB_NAME)}")
    #logger.info(f"DB_HOST: {os.getenv(DB_HOST)}")

    #logger.info(f"CLOUDINARY_ENV_FILE: {CLOUDINARY_ENV_FILE}")
    #logger.info(f"CLOUDINARY_CLOUD_NAME: {os.getenv(CLOUDINARY_CLOUD_NAME)}")
    #logger.info(f"CLOUDINARY_API_KEY: {os.getenv(CLOUDINARY_API_KEY)}")
    #logger.info(f"CLOUDINARY_API_SECRET: {os.getenv(CLOUDINARY_API_SECRET)}")