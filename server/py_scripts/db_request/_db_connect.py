import asyncpg
from config.secret import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST

# Функция для подключения к базе данных
async def get_db_connection():
    return await asyncpg.connect(user=DB_USER, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST)