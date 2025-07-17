import uuid, logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton
from db_request.coloring.publisher import get_publisher_by_id
from db_request.coloring.series import get_series_by_id, get_child_series, get_all_parent_series
from db_request.coloring.volume import get_books_by_series
from tools.sending import send_message

router = Router()
logger = logging.getLogger(__name__)

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
    
    message = f"<b>Серия:</b> {series['full_name_ru']}\n"
    if series['name_ru'] != series['name_en']:
        message += f"({series['name_en']})\n"
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
    message += f"<b>Издатель:</b> {publisher['name_ru']}\n"

    #родительские серии
    buttons_parent_series = []
    if series['parent_series_id']:
        parent_series = await get_all_parent_series(series_id)
        if parent_series:
            message += "\n<b>Находится в серии:</b>\n"
            for parent in parent_series:
                message += f" ∙   {parent['name_ru']}\n"
                buttons_parent_series.append(
                    InlineKeyboardButton(
                        text=parent['name_ru'], 
                        callback_data=PATH_SERIES + str(parent['id']))
                )

    #дочерние серии
    buttons_child_series = []
    child_series = await get_child_series(series_id)
    if child_series:
        message += "\n<b>Содержит серии:</b>\n"
        for child in child_series:
            message += f" ∙   {child['name_ru']}\n"
            buttons_child_series.append(
                InlineKeyboardButton(
                    text=child['name_ru'], 
                    callback_data=PATH_SERIES + str(child['id']))
            )

    #книги в серии
    buttons_books = []
    books = await get_books_by_series(series_id)
    if books:
        message += "\n<b>Книги в серии:</b>\n"
        for book in books:
            message += f" ∙   {book['name_ru']}\n"
            buttons_books.append(
                InlineKeyboardButton(
                    text=book['name_ru'], 
                    callback_data=PATH_BOOK + str(book['id']))
            )

    await send_message(
        message=callback_query.message,
        text=message,
        buttons=(
            buttons_books + buttons_child_series + buttons_parent_series + [button_publisher, BUTTON_MAIN]
        )
    )