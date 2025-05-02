import uuid, copy
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, LoginUrl
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, WebAppInfo, LabeledPrice
from aiogram.types import InputMediaPhoto, FSInputFile
from db_request.publisher import get_publishers, get_publisher_by_id
from db_request.series import get_root_series_by_publisher, get_child_series, get_series_by_id
from db_request.volume import get_books_by_series, get_books_by_publisher_without_series, get_book_by_id
from db_request.cover_file import get_cover_files

router = Router()

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
# BUTTON_PUBLISHER = InlineKeyboardButton(
#     text="Издатель",
#     callback_data=PATH_PUBLISHER)
# BUTTON_SERIES = InlineKeyboardButton(
#     text="Серия",
#     callback_data=PATH_SERIES)
# BUTTON_BOOK = InlineKeyboardButton(
#     text="Книга",
#     callback_data=PATH_BOOK)

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

@router.callback_query(F.data.startswith(PATH_BOOK))
async def handle_book(callback_query: CallbackQuery):    
    try:
        book_id = uuid.UUID(callback_query.data.removeprefix(PATH_BOOK))
    except ValueError:
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
    callback_query.message.delete()
    callback_query.message.answer_photo(
        photo=photo,
        caption=message,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [button_publisher],
            [BUTTON_MAIN]
        ]),
        parse_mode="HTML"
    )      
    

def get_button(button: InlineKeyboardButton, text: str = None, callback_data: str = None) -> InlineKeyboardButton:
    """
    Клонирует кнопку, заменяя текст и/или callback_data
    """
    new_button = copy.deepcopy(button)
    if text is not None:
        new_button.text = text
    if callback_data is not None:
        new_button.callback_data = callback_data
    return new_button