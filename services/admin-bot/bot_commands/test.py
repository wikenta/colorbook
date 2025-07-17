from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
router = Router()

buttons = [
    InlineKeyboardButton(text="Действие 1", callback_data="action:1"),
    InlineKeyboardButton(text="Действие 2", callback_data="action:2"),
    InlineKeyboardButton(text="Уведомление", callback_data="button"),
]

@router.message(F.text == "/test_buttons")
async def test_buttons(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[b] for b in buttons])
    await message.reply("Нажмите кнопку:", reply_markup=keyboard)

@router.callback_query(F.data == "button")
async def handle_button2(callback_query: CallbackQuery):
    await callback_query.answer("Вы получили уведомление!", show_alert=False)

@router.callback_query(F.data.startswith("action:"))
async def handle_action(callback: CallbackQuery):
    action_id = callback.data.split(":")[1]
    await callback.answer(f"Выбрано действие {action_id}", show_alert=True)