import asyncpg, os
from tools.loading import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST

# Функция для подключения к базе данных
async def get_db_connection():
    return await asyncpg.connect(
        user=os.getenv(DB_USER), 
        password=os.getenv(DB_PASSWORD),
        database=os.getenv(DB_NAME),
        host=os.getenv(DB_HOST)
    )