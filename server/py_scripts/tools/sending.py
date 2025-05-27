from aiogram.types import Message
from aiogram.types import InlineKeyboardButton
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest
from typing import Optional
from config.secret import BOT_ID
from .keyboard import get_keyboard
import logging, os, validators
logger = logging.getLogger("colorbook")

def message_from_me(message: Message) -> bool:
    return message.from_user is not None and message.from_user.id == BOT_ID

async def send_message(
        message: Message,
        text: str,
        buttons: Optional[list[InlineKeyboardButton]] = None,
        parse_mode: str = "HTML",
        save_old: bool = False
):
    """
    Сообщение без фото
    """
    try:
        keyboard = get_keyboard(buttons)

        if save_old or not message_from_me(message) or message.media_group_id or message.photo:
            if not save_old:
                try:
                    await message.delete()
                except TelegramBadRequest:
                    logger.error(f"Ошибка при удалении сообщения: {message.message_id}")
            await message.answer(text, parse_mode=parse_mode, reply_markup=keyboard)
        else:
            await message.edit_text(text, parse_mode=parse_mode, reply_markup=keyboard)
    except TelegramBadRequest as e:
        if e.message != "Message is not modified":
            logger.error(f"Ошибка при отправке сообщения: {e}")

def get_photo(path: str) -> FSInputFile | str | None:
    if validators.url(path):
        return path
    elif os.path.isfile(path):
        return FSInputFile(path)
    elif os.path.isfile('/colorbook/files/'+path):
        return FSInputFile('/colorbook/files/'+path)
    else:
        logger.error(f"Файл не найден: {path}")
        return None

async def send_photo(
        message: Message,
        path: str, # локальный путь или URL
        text: str,
        buttons: Optional[list[InlineKeyboardButton]] = None,
        parse_mode: str = "HTML",
        save_old: bool = False
):
    """
    Сообщение с фото
    """
    try:
        if not save_old:
            try:
                await message.delete()
            except TelegramBadRequest:
                logger.error(f"Ошибка при удалении сообщения: {message.message_id}")

        keyboard = get_keyboard(buttons)
        
        photo = get_photo(path)
        if photo:
            await message.answer_photo(
                photo=photo,
                caption=text,
                parse_mode=parse_mode
            )
            await message.answer(
                text="Выберите действие:",
                reply_markup=keyboard,
                parse_mode=parse_mode
            )
        else:
            await message.answer(
                text=text + "\n\nК сожалению, не удалось загрузить фото",
                reply_markup=keyboard,
                parse_mode=parse_mode
            )
    except TelegramBadRequest as e:
        if e.message != "Message is not modified":
            logger.error(f"Ошибка при отправке фото: {e}")

async def send_group_photo(
        message: Message,
        path: list[str], # локальные пути
        text: str,
        buttons: Optional[list[InlineKeyboardButton]] = None,
        parse_mode: str = "HTML",
        save_old: bool = False
):
    """
    Сообщение с несколькими фото
    """
    try:
        if not save_old:
            try:
                await message.delete()
            except TelegramBadRequest:
                logger.error(f"Ошибка при удалении сообщения: {message.message_id}")

        keyboard = get_keyboard(buttons)

        photos = [get_photo(p) for p in path]
        
        missing_photos = [p for p in photos if p is None] 
        if missing_photos:
            logger.error(f"Фото не найдены: {missing_photos}")
            if len(missing_photos) == len(path):
                return
        
        photos = [p for p in photos if p is not None]
        if photos:
            media = [
                InputMediaPhoto(media=photo)
                for photo in photos
            ]
            media[0].caption = text
            media[0].parse_mode = parse_mode
            await message.answer_media_group(media=media)

            await message.answer(
                text="Выберите действие:",
                reply_markup=keyboard,
                parse_mode=parse_mode
            )
        else:
            logger.error("Нет доступных фото для отправки")
            await message.answer(
                text=text + "\n\nК сожалению, не удалось загрузить фото",
                reply_markup=keyboard,
                parse_mode=parse_mode
            )
    except TelegramBadRequest as e:
        if e.message != "Message is not modified":
            logger.error(f"Ошибка при отправке группы фото: {e}")