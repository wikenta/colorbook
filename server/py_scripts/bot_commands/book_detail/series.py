import uuid, logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_request.publisher import get_publisher_by_id
from db_request.series import get_series_by_id

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
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [BUTTON_MAIN]
        ])
        await callback_query.message.edit_text(
            "Некорректный ID серии",
            reply_markup=keyboard, 
            parse_mode="HTML")
        return

    series = await get_series_by_id(series_id)
    if not series:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [BUTTON_MAIN]
        ])
        await callback_query.message.edit_text(
            "Серия не найдена",
            reply_markup=keyboard, 
            parse_mode="HTML")
        return
    
    message = f"Серия: {series['full_name_ru']}\n"
    publisher_id = series['publisher_id']
    publisher = await get_publisher_by_id(publisher_id)
    if not publisher:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [BUTTON_MAIN]
        ])
        await callback_query.message.edit_text(
            message + "Издатель не найден",
            reply_markup=keyboard, 
            parse_mode="HTML")
        return
    
    button_publisher = InlineKeyboardButton(
        text=publisher['name_ru'], 
        callback_data=PATH_PUBLISHER + str(publisher_id))
    message += f"Издатель: {publisher['name_ru']}\n"
    await callback_query.message.edit_text(
        message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [button_publisher],
            [BUTTON_MAIN]
        ]),
        parse_mode="HTML"
    )