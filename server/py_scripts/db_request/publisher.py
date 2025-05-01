from asyncpg import Record
from typing import Optional, List
from db_request.db_connect import get_db_connection

async def get_publishers() -> List[Record]:
    """
    Все издатели: id, name_en и name_ru
    """
    conn = await get_db_connection()
    publishers = await conn.fetch("SELECT id, name_en, name_ru FROM coloring.publisher ORDER BY name_ru")
    await conn.close()
    return publishers

async def get_publisher_by_id(publisher_id: str) -> Optional[Record]:
    """
    Издатель по ID: id, name_en и name_ru
    """
    conn = await get_db_connection()
    query = "SELECT id, name_ru, name_en FROM coloring.publisher WHERE id = $1"
    publisher = await conn.fetchrow(query, publisher_id)
    await conn.close()
    return publisher