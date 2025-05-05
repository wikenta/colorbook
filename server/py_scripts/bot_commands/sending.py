from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest
from typing import Optional
import logging, os
logger = logging.getLogger("colorbook")

async def send_message(
        message: Message,
        text: str,
        buttons: Optional[list[InlineKeyboardButton]] = None,
        parse_mode: str = "HTML",
        new_answer: bool = False
):
    """
    Сообщение без фото
    """
    try:
        keyboard = None
        if buttons:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [b] for b in buttons]
            )

        if new_answer or message.media_group_id:
            await message.answer(text, parse_mode=parse_mode, reply_markup=keyboard, reply_parameters=None)
        elif message.photo:
            try:
                await message.delete()
            except TelegramBadRequest:
                logger.error(f"Ошибка при удалении сообщения: {message.message_id}")
            await message.answer(text, parse_mode=parse_mode, reply_markup=keyboard, reply_parameters=None)
        else:
            await message.edit_text(text, parse_mode=parse_mode, reply_markup=keyboard)

    except TelegramBadRequest as e:
        if e.message != "Message is not modified":
            logger.error(f"Ошибка при отправке сообщения: {e}")

async def send_photo(
        message: Message,
        path: str, # локальный путь
        text: str,
        buttons: Optional[list[InlineKeyboardButton]] = None,
        parse_mode: str = "HTML",
        new_answer: bool = False
):
    """
    Сообщение с фото
    """
    try:
        if os.path.isfile(path):
            photo = FSInputFile(path)
        else:
            logger.error(f"Файл не найден: {path}")
            return

        keyboard = None
        if buttons:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [b] for b in buttons]
            )

        if new_answer or message.media_group_id:
            await message.answer_photo(
                photo=photo,
                caption=text,
                parse_mode=parse_mode,
                reply_markup=keyboard, 
                reply_parameters=None
            )
        elif message.photo:
            media = InputMediaPhoto(
                media=photo,
                caption=text,
                parse_mode=parse_mode
            )
            await message.edit_media(
                media=media,
                reply_markup=keyboard
            )
        else:
            try:
                await message.delete()
            except TelegramBadRequest:
                logger.error(f"Ошибка при удалении сообщения: {message.message_id}")
            await message.answer_photo(
                photo=photo,
                caption=text,
                parse_mode=parse_mode,
                reply_markup=keyboard, 
                reply_parameters=None
            )
    except TelegramBadRequest as e:
        if e.message != "Message is not modified":
            logger.error(f"Ошибка при отправке фото: {e}")

async def send_group_photo(
        message: Message,
        path: list[str], # локальные пути
        text: str,
        parse_mode: str = "HTML",
        new_answer: bool = False
):
    """
    Сообщение с несколькими фото
    """
    try:
        missing_files = [photo for photo in path if not os.path.isfile(photo)]
        if missing_files:
            logger.error(f"Файлы не найдены: {missing_files}")
            if len(missing_files) == len(path):
                return
        valid_files = [photo for photo in path if os.path.isfile(photo)]
        if not valid_files:
            logger.error("Нет доступных файлов для отправки")
            return
        
        media = [
            InputMediaPhoto(media=FSInputFile(photo))
            for photo in valid_files
        ]
        media[0].caption = text
        media[0].parse_mode = parse_mode

        if not new_answer and not message.media_group_id:
            try:
                await message.delete()
            except TelegramBadRequest:
                logger.error(f"Ошибка при удалении сообщения: {message.message_id}")
        await message.answer_media_group(media=media)
    except TelegramBadRequest as e:
        if e.message != "Message is not modified":
            logger.error(f"Ошибка при отправке группы фото: {e}")