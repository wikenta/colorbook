from aiogram import F, Router
from aiogram.types import Message
from db_request.publisher import get_publishers
from db_request.series import get_root_series_by_publisher, get_child_series
from db_request.volume import get_books_by_series, get_books_by_publisher_without_series
from .sending import send_message
import logging
logger = logging.getLogger("colorbook")

router = Router()

# Отображение списка всех книг
@router.message(F.text == "/books")
async def send_books(message: Message):
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения: {e}")

    publishers = await get_publishers()
    if not publishers:
        await send_message(message, "Издатели не найдены.")
        return
    
    for publisher in publishers:
        series = await get_root_series_by_publisher(publisher['id'])
        books = await get_books_by_publisher_without_series(publisher['id'])
        if not series and not books:
            continue

        response = f"Издатель: {publisher['name_ru']}\n"
        for s in series:
            response += f"\n<b>{s['name_ru']}</b>\n"
            response += await get_message_child_series_recursive(s['id'])
        if books:
            response += "\n<b>Книги без серии:</b>\n"
            for book in books:
                response += f" ∙   {book['name_ru']}"
                if book['release_year']:
                    response += f" ({book['release_year']})"
                response += "\n"
        await send_message(message, response, save_old = True)

async def get_message_child_series_recursive (series_id: str, depth: int = 0) -> str:
    """
    Рекурсивно получает дочерние серии и формирует сообщение
    """
    books = await get_books_by_series(series_id)
    series = await get_child_series(series_id)
    if not series and not books:
        return f"{'   ' * depth}     Не заполнено\n"

    response = ""
    for book in books:
        response += f"{'   ' * depth} ∙   {book['name_ru']}"
        if book['release_year']:
            response += f" ({book['release_year']})"
        response += "\n"
    
    for child in series:
        response += f"{'   ' * depth} ⤷ <b>{child['name_ru']}</b>\n"
        response += await get_message_child_series_recursive(child['id'], depth + 1)

    return response