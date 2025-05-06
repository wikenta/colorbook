from aiogram import F, Router
from aiogram.types import Message
from .sending import send_message
router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.delete()
    text = (
        "Приветствую!\n"
        "\n"
        "Доступно сейчас:\n"
        " - посмотреть список выпущенных книг (дополняется)\n"
        "\n"
        "В процессе разработки:\n"
        " - загрузить обложки книг\n"
        "\n"
        "Планируется:\n"
        " - заполнить список иллюстраций в книгах (в самых популярных для начала)\n"
        " - загрузить изображения готовых страниц из раздела \"решения\"\n"
        " - добавить возможность оставить сообщение разработчику (мне)\n"
        "\n"
        "Это только ближайшие планы, в целом я крайне амбициозна. "
        "Но заполнение требует много времени, мне будет нужна помощь энтузиастов"
    )
    await send_message(message, text, new_answer=True)