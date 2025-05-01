from aiogram import F, Router
import asyncio
from aiogram.types import Message, CallbackQuery, LoginUrl
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, WebAppInfo, LabeledPrice
from db_request.publisher import get_publishers
from db_request.series import get_root_series_by_publisher, get_child_series
from db_request.volume import get_books_by_series

router = Router()

# Точка входа
@router.message(F.text == "/book_detail")
async def send_book_detail(message: Message):
    await show_publishers(message, first_message=True)

# когда пользователь нажимает "вернуться к издателям", показываем список издателей
@router.callback_query(F.data == "back_to_publishers")
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
    
    buttons = [
        [InlineKeyboardButton(text=publisher['name_ru'], callback_data=f"publisher_{publisher['id']}")]
        for publisher in publishers
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    if first_message:
        await message.answer(response, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.edit_text(response, reply_markup=keyboard, parse_mode="HTML")

# когда пользователь выбирает издателя:
# показываем кнопку "вернуться к издателям"
# пишем в сообщении: "Id издателя: {id}"
# Id в базе данных UUID
@router.callback_query(F.data.startswith("publisher_"))
async def handle_publisher(callback_query: CallbackQuery):
    publisher_id = callback_query.data.split("_")[1]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться к издателям", callback_data="back_to_publishers")]
    ])
    await callback_query.message.edit_text(
        f"Id издателя: {publisher_id}",
        reply_markup=keyboard,
        parse_mode="HTML"
    )