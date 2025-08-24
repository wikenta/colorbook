from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from .start import router as start_router
from .load_image import router as load_image_router
from .test import router as test_router

def register_routers(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(load_image_router)
    dp.include_router(test_router)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Приветствие"),
        BotCommand(command="load_image", description="Загрузка изображения"),
        BotCommand(command="test_buttons", description="Тест кнопок")
    ]
    await bot.set_my_commands(commands)