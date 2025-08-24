from aiogram import F, Router
from aiogram.types import Message
from tools.sending import send_message
from tools.loading import ADMIN_TG_ID, TELEGRAM_BOT_ID, TELEGRAM_BOT_LOGIN, TELEGRAM_API_TOKEN, DB_NAME, CLOUDINARY_CLOUD_NAME
import os, logging

router = Router()
logger = logging.getLogger(__name__)

#я получаю команду, прошу загрузить изображение
#в ответ получаю изображение
@router.message(F.text == "/load_image")
async def cmd_load_image(message: Message):
    ADMIN_ID = os.getenv(ADMIN_TG_ID)
    if ADMIN_ID is not None:
        logger.info(f"Admin ID loaded: {ADMIN_ID}")
    else:
        logger.error("ADMIN_TG_ID is not set in environment variables.")
    TG_BOT_ID = os.getenv(TELEGRAM_BOT_ID)
    if TG_BOT_ID is not None:
        logger.info(f"Bot ID loaded: {TG_BOT_ID}")
    else:
        logger.error("TELEGRAM_BOT_ID is not set in environment variables.")
    TG_BOT_LOGIN = os.getenv(TELEGRAM_BOT_LOGIN)
    if TG_BOT_LOGIN is not None:
        logger.info(f"Bot login loaded: {TG_BOT_LOGIN}")
    else:
        logger.error("TELEGRAM_BOT_LOGIN is not set in environment variables.")
    TG_API_TOKEN = os.getenv(TELEGRAM_API_TOKEN)
    if TG_API_TOKEN is not None:
        logger.info("API token loaded successfully.")
    else:
        logger.error("TELEGRAM_API_TOKEN is not set in environment variables.")
    DB_NAME = os.getenv(DB_NAME)
    if DB_NAME is not None:
        logger.info(f"Database name loaded: {DB_NAME}")
    else:
        logger.error("DB_NAME is not set in environment variables.")
    CLOUD_NAME = os.getenv(CLOUDINARY_CLOUD_NAME)
    if CLOUD_NAME is not None:
        logger.info(f"Cloudinary cloud name loaded: {CLOUD_NAME}")
    else:
        logger.error("CLOUDINARY_CLOUD_NAME is not set in environment variables.")

    if str(message.from_user.id) != ADMIN_ID:
        await message.reply(
            "Здесь можно настраивать бот, но вы не администратор."
            "Воспользоваться ботом можно здесь:\n"
            "@color_book_bot"
        )
        logger.warning(f"Unauthorized access attempt by user ID: {message.from_user.id}, "+
                       f"admin ID: {ADMIN_ID}")
        return
    text = (
        "Загрузите изображение\n\n"
    )
    logger.info(f"Admin {ADMIN_ID} initiated image load.")
    await send_message(message, text)
    # await message.reply("Пожалуйста, отправьте изображение, которое хотите загрузить.")

@router.message(F.photo)
async def handle_photo(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    #присылаю это же фото в ответ
    await message.answer_photo(photo=message.photo[-1].file_id, caption="Вот ваше изображение!")
    await message.reply("В какой том хотите добавить изображение?")