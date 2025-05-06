from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from .start import router as start_router
from .books import router as books_router
from .book_detail.publisher import router as book_detail_publisher_router
from .book_detail.series import router as book_detail_series_router
from .book_detail.book import router as book_detail_book_router

def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(books_router)
    dp.include_router(book_detail_publisher_router)
    dp.include_router(book_detail_series_router)
    dp.include_router(book_detail_book_router)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Приветствие"),
        BotCommand(command="books", description="Показать список книг"),
        BotCommand(command="book_detail", description="Показать подробную информацию о книге")
    ]
    await bot.set_my_commands(commands)