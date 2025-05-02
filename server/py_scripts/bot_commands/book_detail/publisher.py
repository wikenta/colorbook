import uuid, logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db_request.publisher import get_publishers, get_publisher_by_id
from db_request.series import get_root_series_by_publisher
from db_request.volume import get_books_by_publisher_without_series

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
    await show_publishers(message, first_message=True)

# когда пользователь нажимает "вернуться к издателям", показываем список издателей
@router.callback_query(F.data == PATH_MAIN)
async def back_to_publishers(callback_query: CallbackQuery):
    await show_publishers(callback_query.message)

# показать первое сообщение: список издателей
async def show_publishers(message: Message, first_message: bool = False):
    publishers = await get_publishers()
    if not publishers:
        if first_message:
            await message.answer("Издатели не найдены.")
        else:
            await message.edit_text("Издатели не найдены.")
        return
    
    response = "Выберите издателя:\n\n"
    for publisher in publishers:
        response += f" ∙   {publisher['name_ru']}\n"
    
    publisher_buttons = [
        [InlineKeyboardButton(
            text=publisher['name_ru'], 
            callback_data=PATH_PUBLISHER + str(publisher['id']))]
        for publisher in publishers
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=publisher_buttons)
    if first_message:
        await message.answer(response, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.edit_text(response, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data.startswith(PATH_PUBLISHER))
async def handle_publisher(callback_query: CallbackQuery):    
    try:
        publisher_id = uuid.UUID(callback_query.data.removeprefix(PATH_PUBLISHER))
    except ValueError:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [BUTTON_MAIN]
        ])
        await callback_query.message.edit_text(
            "Некорректный ID издателя",
            reply_markup=keyboard, 
            parse_mode="HTML")
        return

    publisher = await get_publisher_by_id(publisher_id)
    if not publisher:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [BUTTON_MAIN]
        ])
        await callback_query.message.edit_text(
            "Издатель не найден",
            reply_markup=keyboard, 
            parse_mode="HTML")
        return
    
    message = f"Издатель: {publisher['name_ru']}\n\n"
    series = await get_root_series_by_publisher(publisher_id)
    books = await get_books_by_publisher_without_series(publisher_id)
    if not series and not books:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [BUTTON_MAIN]
        ])
        await callback_query.message.edit_text(
            message + "У этого издателя не заполнены книги",
            reply_markup=keyboard, 
            parse_mode="HTML")
        return
    
    if series:
        message += "Серии:\n"
        for s in series:
            message += f" ∙   {s['name_ru']}\n"
        message += "\n"
    if books:
        message += "Книги без серии:\n"
        for book in books:
            message += f" ∙   {book['name_ru']}\n"
        message += "\n"

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
    buttons = buttons[:9] + [BUTTON_MAIN]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [button] for button in buttons
    ])

    await callback_query.message.edit_text(
        message,
        reply_markup=keyboard,
        parse_mode="HTML"
    )   
