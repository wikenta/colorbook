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
    if str(message.from_user.id) != os.getenv(ADMIN_TG_ID):
        await message.reply(
            "Здесь можно настраивать бот, но вы не администратор."
            "Воспользоваться ботом можно здесь:\n"
            "@color_book_bot"
        )
        return
    text = (
        "Загрузите изображение\n\n"
    )
    logging.warning(f"Admin {message.from_user.id} ({message.from_user.full_name}) initiated /load_image")
    await send_message(message, text)

@router.message(F.photo)
async def handle_photo(message: Message):
    if str(message.from_user.id) != os.getenv(ADMIN_TG_ID):
        return
    #присылаю это же фото в ответ
    await message.answer_photo(photo=message.photo[-1].file_id, caption="Вот ваше изображение!")
    await message.reply("В какой том хотите добавить изображение?")