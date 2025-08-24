from aiogram import F, Router
from aiogram.types import Message
from tools.sending import send_message
from tools.loading import ADMIN_TG_ID
import os

router = Router()
ADMIN_ID = os.getenv(ADMIN_TG_ID)

#я получаю команду, прошу загрузить изображение
#в ответ получаю изображение
@router.message(F.text == "/load_image")
async def cmd_load_image(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply(
            "Здесь можно настраивать бот, но вы не администратор."
            "Воспользоваться ботом можно здесь:\n"
            "@color_book_bot"
        )
        return
    text = (
        "Загрузите изображение\n\n" +
        "Кстати, ваш id: " + str(message.from_user.id)
    )
    await send_message(message, text)
    # await message.reply("Пожалуйста, отправьте изображение, которое хотите загрузить.")

@router.message(F.photo)
async def handle_photo(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    #присылаю это же фото в ответ
    await message.answer_photo(photo=message.photo[-1].file_id, caption="Вот ваше изображение!")
    await message.reply("В какой том хотите добавить изображение?")