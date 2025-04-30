from aiogram import Router, Bot
from aiogram.types import BotCommand

router = Router()

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="books", description="Показать список книг"),
        #BotCommand(command="books_test", description="Показать новый список книг"),
        #BotCommand(command="test_buttons", description="Тест Inline-кнопок"),
        #BotCommand(command="test_reply_buttons", description="Тест Reply-кнопок"),
        #BotCommand(command="remove_buttons", description="Удалить клавиатуру"),
        #BotCommand(command="test_force_reply", description="Принудительный ответ"),
        #BotCommand(command="test_callback_args", description="Кнопки с аргументами"),
        #BotCommand(command="test_emoji_buttons", description="Кнопки с эмодзи"),
        #BotCommand(command="test_webapp", description="Тест WebApp"),
        #BotCommand(command="test_payment", description="Тест оплаты (демо)"),
        #BotCommand(command="test_timer_button", description="Кнопка с таймером")
    ]
    await bot.set_my_commands(commands)