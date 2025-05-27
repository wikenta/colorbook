from asyncpg import Record
from typing import Optional, List
from ._db_connect import get_db_connection

async def get_cover_files(volume_id: str) -> List[Record]:
    """
    Все файлы обложек тома: file_path
    """
    conn = await get_db_connection()
    query = """
    SELECT c.id, c.file_path
    FROM files.cover_file c WHERE c.volume_id = $1
    """
    cover_files = await conn.fetch(query, volume_id)
    await conn.close()
    return cover_files