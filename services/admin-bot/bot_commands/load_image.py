from aiogram import F, Router
from aiogram.types import Message
from tools.sending import send_message
router = Router()

#я получаю команду, прошу загрузить изображение
#в ответ получаю изображение
@router.message(F.text == "/load_image")
async def cmd_load_image(message: Message):
    text = (
        "Загрузите изображение\n\n" +
        "Кстати, ваш id: " + str(message.from_user.id)
    )
    await send_message(message, text)
    # await message.reply("Пожалуйста, отправьте изображение, которое хотите загрузить.")

@router.message(F.photo)
async def handle_photo(message: Message):
    #присылаю это же фото в ответ
    await message.answer_photo(photo=message.photo[-1].file_id, caption="Вот ваше изображение!")
    await message.reply("В какой том хотите добавить изображение?")