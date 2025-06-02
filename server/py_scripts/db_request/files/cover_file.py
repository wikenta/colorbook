from asyncpg import Record
from typing import Optional, List
from .._db_connect import get_db_connection

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

async def update_cover_file_path(cover_id: str, new_file_path: str) -> Optional[Record]:
    """
    Обновить путь к файлу обложки по ID
    """
    conn = await get_db_connection()
    query = """
    UPDATE files.cover_file
    SET file_path = $1
    WHERE id = $2
    RETURNING id, file_path
    """
    updated_cover = await conn.fetchrow(query, new_file_path, cover_id)
    await conn.close()
    return updated_cover