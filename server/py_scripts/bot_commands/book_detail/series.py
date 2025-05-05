import uuid, logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_request.publisher import get_publisher_by_id
from db_request.series import get_series_by_id
from ..sending import send_message

router = Router()
logger = logging.getLogger("colorbook")

# Пути, используемые в этом файле:
PATH_ENTRY_POINT = "/book_detail"
PATH_MAIN = "detail_publishers"
PATH_PUBLISHER = "detail_publisher_"
PATH_SERIES = "detail_series_"
PATH_BOOK = "detail_book_"

# Стандартные кнопки
BUTTON_MAIN = InlineKeyboardButton(
    text="Издатели",
    callback_data=PATH_MAIN)

@router.callback_query(F.data.startswith(PATH_SERIES))
async def handle_series(callback_query: CallbackQuery):    
    try:
        series_id = uuid.UUID(callback_query.data.removeprefix(PATH_SERIES))
    except ValueError:
        await send_message(
            message=callback_query.message,
            text="Некорректный ID серии",
            buttons=[BUTTON_MAIN],
        )
        return

    series = await get_series_by_id(series_id)
    if not series:
        await send_message(
            message=callback_query.message,
            text="Серия не найдена",
            buttons=[BUTTON_MAIN],
        )
        return
    
    message = f"Серия: {series['full_name_ru']}\n"
    publisher_id = series['publisher_id']
    publisher = await get_publisher_by_id(publisher_id)
    if not publisher:
        await send_message(
            message=callback_query.message,
            text="Издатель не найден",
            buttons=[BUTTON_MAIN],
        )
        return
    
    button_publisher = InlineKeyboardButton(
        text=publisher['name_ru'], 
        callback_data=PATH_PUBLISHER + str(publisher_id))
    message += f"Издатель: {publisher['name_ru']}\n"
    await send_message(
        message=callback_query.message,
        text=message,
        buttons=[button_publisher, BUTTON_MAIN],
    )