import uuid, logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton
from db_request.publisher import get_publishers, get_publisher_by_id
from db_request.series import get_root_series_by_publisher
from db_request.volume import get_books_by_publisher_without_series
from tools.sending import send_message

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

# Точка входа
@router.message(F.text == PATH_ENTRY_POINT)
async def send_book_detail(message: Message):
    await show_publishers(message)

# когда пользователь нажимает "вернуться к издателям", показываем список издателей
@router.callback_query(F.data == PATH_MAIN)
async def back_to_publishers(callback_query: CallbackQuery):
    await show_publishers(callback_query.message)

# показать первое сообщение: список издателей
async def show_publishers(message: Message):
    publishers = await get_publishers()
    if not publishers:
        await send_message( 
            message=message, 
            text="Издатели не найдены.")
        return
    
    response = "Выберите издателя:\n\n"
    for publisher in publishers:
        response += f" ∙   {publisher['name_ru']}\n"
    
    buttons = [
        InlineKeyboardButton(
            text=publisher['name_ru'], 
            callback_data=PATH_PUBLISHER + str(publisher['id']))
        for publisher in publishers
    ]
    await send_message(
        message=message,
        text=response,
        buttons=buttons
    )

@router.callback_query(F.data.startswith(PATH_PUBLISHER))
async def handle_publisher(callback_query: CallbackQuery):    
    try:
        publisher_id = uuid.UUID(callback_query.data.removeprefix(PATH_PUBLISHER))
    except ValueError:
        await send_message(
            message=callback_query.message,
            text="Некорректный ID издателя",
            buttons=[BUTTON_MAIN]
        )
        return

    publisher = await get_publisher_by_id(publisher_id)
    if not publisher:
        await send_message(
            message=callback_query.message,
            text="Издатель не найден",
            buttons=[BUTTON_MAIN]
        )
        return
    
    message = f"<b>Издатель:</b> {publisher['name_ru']}\n"
    series = await get_root_series_by_publisher(publisher_id)
    books = await get_books_by_publisher_without_series(publisher_id)
    if not series and not books:
        await send_message(
            message=callback_query.message,
            text="У этого издателя не заполнены книги",
            buttons=[BUTTON_MAIN]
        )
        return
    
    if series:
        message += "\n<b>Серии:</b>\n"
        for s in series:
            message += f" ∙   {s['name_ru']}\n"
    if books:
        message += "\n<b>Книги без серии:</b>\n"
        for book in books:
            message += f" ∙   {book['name_ru']}\n"

    buttons_series = [
        InlineKeyboardButton(
            text=s['name_ru'], 
            callback_data=PATH_SERIES + str(s['id']))
        for s in series
    ]
    buttons_books = [
        InlineKeyboardButton(
            text=book['name_ru'], 
            callback_data=PATH_BOOK + str(book['id']))
        for book in books
    ]
    buttons = buttons_series + buttons_books
    # первые 9 кнопок + кнопка "вернуться к издателям"
    buttons = buttons + [BUTTON_MAIN]
    
    await send_message(
        message=callback_query.message,
        text=message,
        buttons=buttons
    )
