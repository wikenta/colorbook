#!/usr/bin/env python3
import asyncio, logging, os, signal
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from bot_commands._commands import register_routers, set_commands
from tools.loading import load_environment, TELEGRAM_API_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Let's go! Еху!")

# Загрузка переменных окружения
load_environment() 

# Объекты бота и диспетчера
default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=os.getenv(TELEGRAM_API_TOKEN), default=default_properties)

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
register_routers(dp)

async def shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()  # Опционально: удалить команды при остановке
    await dispatcher.storage.close()
    await bot.session.close()

async def main():
    try:
        await set_commands(bot)
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user (SIGINT/SIGTERM)")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        await shutdown(dp, bot)

if __name__ == '__main__':
    # Обработка сигналов (для корректного завершения)
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown(dp, bot)))

    try:
        loop.run_until_complete(main())
    finally:
        loop.close()