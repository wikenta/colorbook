from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional

def get_keyboard(buttons: Optional[list[InlineKeyboardButton]] = None, count_in_row: int = 2) -> Optional[InlineKeyboardBuilder]:
    """
    Создает клавиатуру из списка кнопок
    """
    keyboard = None
    if buttons:
        builder = InlineKeyboardBuilder()
        builder.add(*buttons)
        if count_in_row > 0:
            builder.adjust(count_in_row)
        keyboard = builder.as_markup()
    return keyboard