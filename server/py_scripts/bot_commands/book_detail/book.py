import uuid, logging
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile
from db_request.publisher import get_publisher_by_id
from db_request.volume import get_book_by_id
from db_request.cover_file import get_cover_files

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
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [BUTTON_MAIN]
        ])
        await callback_query.message.edit_text(
            "Некорректный ID книги",
            reply_markup=keyboard, 
            parse_mode="HTML")
        return

    book = await get_book_by_id(book_id)
    if not book:
        logger.error(f"Книга не найдена: {book_id}")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [BUTTON_MAIN]
        ])
        await callback_query.message.edit_text(
            "Книга не найдена",
            reply_markup=keyboard, 
            parse_mode="HTML")
        return
    
    message = f"Книга: {book['full_name_ru']}\n\n"
    # серия может быть NULL
    publisher_id = book['publisher_id']
    publisher = await get_publisher_by_id(publisher_id)
    if not publisher:
        logger.error(f"Издатель не найден: {publisher_id}")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [BUTTON_MAIN]
        ])
        await callback_query.message.edit_text(
            message + "Издатель не найден",
            reply_markup=keyboard, 
            parse_mode="HTML")
        return
    message += f"Издатель: {publisher['name_ru']}\n"

    button_publisher = InlineKeyboardButton(
        text=publisher['name_ru'], 
        callback_data=PATH_PUBLISHER + str(publisher_id))
    
    covers = await get_cover_files(book_id)
    if not covers:
        logger.error(f"Обложка не найдена: {book_id}")
        await callback_query.message.edit_text(
            message,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [button_publisher],
                [BUTTON_MAIN]
            ]),
            parse_mode="HTML"
        )
        return
    
    photo = FSInputFile('/colorbook/files/'+covers[0]['file_path'])
    logger.info(f"Обложка найдена: {photo.path}")
    await callback_query.message.delete()
    logger.info(f"Сообщение удалено: {callback_query.message.message_id}")
    await callback_query.message.answer_photo(
        photo=photo,
        caption=message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [button_publisher],
            [BUTTON_MAIN]
        ]),
        parse_mode="HTML"
    )
    logger.info(f"Сообщение отправлено: {callback_query.message.message_id}")