from aiogram import F, Router
from aiogram.types import Message
from tools.sending import send_message
router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    text = (
        "Приветствую!\n"
        "\n"
        "Доступно сейчас:\n"
        " - запустить этот бот :)\n"
        "\n"
        "В процессе разработки:\n"
        " - пока создала бот, вот-вот приступлю к следующим шагам\n"
        "\n"
        "Планируется:\n"
        " - спроектировать новую иерархию каталогов в облаке, где хранятся обложки\n"
        " - написать команду для загрузки обложки в облако\n"
        " - написать команду для загрузки промо-материала в облако\n"
        "\n"
        "Все это с выбором конкретной книги, чтобы было удобно\n"
    )
    await send_message(message, text)