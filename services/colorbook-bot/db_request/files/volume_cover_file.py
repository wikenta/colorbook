from asyncpg import Record
from typing import Optional, List
from .._db_connect import get_db_connection
TABLE_NAME = "files.volume_cover_file"

async def get_volume_cover_files(volume_id: str) -> List[Record]:
    """
    Все файлы обложек тома: file_path
    """
    conn = await get_db_connection()
    query = f"""
    SELECT c.id, c.file_path
    FROM {TABLE_NAME} c WHERE c.volume_id = $1
    """
    cover_files = await conn.fetch(query, volume_id)
    await conn.close()
    return cover_files

async def update_volume_cover_file_path(cover_id: str, new_file_path: str) -> Optional[Record]:
    """
    Обновить путь к файлу обложки по ID
    """
    conn = await get_db_connection()
    query = f"""
    UPDATE {TABLE_NAME}
    SET file_path = $1
    WHERE id = $2
    RETURNING id, file_path
    """
    updated_cover = await conn.fetchrow(query, new_file_path, cover_id)
    await conn.close()
    return updated_cover