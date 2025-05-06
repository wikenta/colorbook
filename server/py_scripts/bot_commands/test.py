from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
router = Router()

buttons = [
    [InlineKeyboardButton(text="Всплывающее сообщение", callback_data="button1")],
    [InlineKeyboardButton(text="Уведомление", callback_data="button2")],
    [InlineKeyboardButton(text="Действие 1", callback_data="action:1")],
    [InlineKeyboardButton(text="Действие 2", callback_data="action:2")]
]

# Тестируем кнопки
@router.message(F.text == "/test_buttons")
async def test_buttons(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.reply("Выберите кнопку:", reply_markup=keyboard)

@router.callback_query(F.data == "button1")
async def handle_button1(callback_query: CallbackQuery):
    await callback_query.answer("Вы нажали кнопку 1!", show_alert=True)
    # Вместо удаления клавиатуры - редактируем сообщение
    await callback_query.message.edit_text(
        "Вы выбрали Кнопку 1!\nХотите сделать что-то еще?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Вернуться", callback_data="back_to_menu")]
        ])
    )

@router.callback_query(F.data == "button2")
async def handle_button2(callback_query: CallbackQuery):
    await callback_query.answer("Вы нажали кнопку 2!", show_alert=False)  # Всплывающее уведомление

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback_query: CallbackQuery):
    # Возвращаем исходное меню
    await callback_query.message.edit_text(
        "Выберите кнопку:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

@router.callback_query(F.data.startswith("action:"))
async def handle_action(callback: CallbackQuery):
    action_id = callback.data.split(":")[1]
    await callback.answer(f"Выбрано действие {action_id}", show_alert=True)