from asyncpg import Record
from typing import Optional, List
from db_request.db_connect import get_db_connection

async def get_cover_files(volume_id: str) -> List[Record]:
    """
    Все файлы обложек тома: id, file_path
    """
    conn = await get_db_connection()
    query = """
    SELECT c.id, c.file_path
    FROM files.cover_file c
    """
    cover_files = await conn.fetch(query)
    await conn.close()
    return cover_files