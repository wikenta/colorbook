import uuid, logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton
from db_request.coloring.publisher import get_publisher_by_id
from db_request.coloring.series import get_series_by_id, get_all_parent_series
from db_request.coloring.volume import get_book_by_id
from db_request.files.volume_cover_file import get_volume_cover_files
from tools.sending import send_message, send_photo

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

@router.callback_query(F.data.startswith(PATH_BOOK))
async def handle_book(callback_query: CallbackQuery):    
    try:
        book_id = uuid.UUID(callback_query.data.removeprefix(PATH_BOOK))
    except ValueError:
        logger.error(f"Некорректный ID книги: {callback_query.data}")
        await send_message(
            message=callback_query.message,
            text="Некорректный ID книги",
            buttons=[BUTTON_MAIN]
        )
        return

    book = await get_book_by_id(book_id)
    if not book:
        logger.error(f"Книга не найдена: {book_id}")
        await send_message(
            message=callback_query.message,
            text="Книга не найдена",
            buttons=[BUTTON_MAIN]
        )
        return
    
    message = f"<b>Книга:</b> {book['full_name_ru']}\n"
    if book['name_ru'] != book['name_en']:
        message += f"({book['name_en']})\n"
    message += "\n"
    publisher_id = book['publisher_id']
    publisher = await get_publisher_by_id(publisher_id)
    if not publisher:
        logger.error(f"Издатель не найден: {publisher_id}")
        await send_message(
            message=callback_query.message,
            text=message + "Издатель не найден",
            buttons=[BUTTON_MAIN]
        )
        return
    message += f"<b>Издатель:</b> {publisher['name_ru']}\n"

    button_publisher = InlineKeyboardButton(
        text=publisher['name_ru'], 
        callback_data=PATH_PUBLISHER + str(publisher_id))
    
    # год издания
    if book['release_year']:
        message += f"<b>Год издания:</b> {book['release_year']}\n"
    
    # серия может быть NULL
    buttons_series = []
    if book['series_id']:
        series = await get_series_by_id(book['series_id'])
        if series:
            message += f"<b>Серия:</b> {series['full_name_ru']}\n"
            buttons_series.append(
                InlineKeyboardButton(
                    text=series['name_ru'], 
                    callback_data=PATH_SERIES + str(series['id']))
            )
            if series['parent_series_id']:
                parent_series = await get_all_parent_series(series['id'])
                if parent_series:
                    for parent in parent_series:
                        buttons_series.append(
                            InlineKeyboardButton(
                                text=parent['name_ru'], 
                                callback_data=PATH_SERIES + str(parent['id']))
                        )
        else:
            logger.error(f"Серия не найдена: {book['series_id']}")

    covers = await get_volume_cover_files(book_id)
    if covers:
        path = covers[0]['file_path']
        await send_photo(
            message=callback_query.message,
            path=path,
            text=message,
            buttons=(buttons_series + [button_publisher, BUTTON_MAIN])
        )
    else:
        logger.error(f"Обложка не найдена: {book_id}")
        await send_message(
            message=callback_query.message,
            text=message,
            buttons=(buttons_series + [button_publisher, BUTTON_MAIN])
        )
