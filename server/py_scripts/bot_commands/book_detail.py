from aiogram import F, Router
import asyncio
from aiogram.types import Message, CallbackQuery, LoginUrl
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, WebAppInfo, LabeledPrice
from db_request.publisher import get_publishers
from db_request.series import get_root_series_by_publisher, get_child_series
from db_request.volume import get_books_by_series

router = Router()

# Отображение подробной информации о книге
@router.message(F.text == "/book_detail")
async def send_book_detail(message: Message):
    show_publishers(message)

# показать первое сообщение: список издателей
async def show_publishers(message: Message):
    publishers = await get_publishers()
    if not publishers:
        await message.reply("Издатели не найдены.")
        return
    
    response = "Выберите издателя:\n\n"
    for publisher in publishers:
        response += f" ∙   {publisher['name_ru']}\n"        
    
    await message.reply(response, parse_mode="HTML")