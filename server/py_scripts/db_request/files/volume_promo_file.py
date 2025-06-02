from asyncpg import Record
from typing import Optional, List
from .._db_connect import get_db_connection
TABLE_NAME = "files.volume_promo_file"

async def get_volume_promo_files(volume_id: str) -> List[Record]:
    """
    Все файлы тома: file_path
    """
    conn = await get_db_connection()
    query = f"""
    SELECT c.id, c.file_path, c.number
    FROM {TABLE_NAME} c WHERE c.volume_id = $1
    """
    cover_files = await conn.fetch(query, volume_id)
    await conn.close()
    return cover_files

async def update_volume_promo_file_path(promo_id: str, new_file_path: str) -> Optional[Record]:
    """
    Обновить путь к файлу по ID
    """
    conn = await get_db_connection()
    query = f"""
    UPDATE {TABLE_NAME}
    SET file_path = $1
    WHERE id = $2
    RETURNING id, file_path
    """
    updated_cover = await conn.fetchrow(query, new_file_path, promo_id)
    await conn.close()
    return updated_cover

async def create_volume_promo_file(volume_id: str, file_path: str, number: Optional[int] = None) -> Record:
    """
    Создать новую запись файла промо-материала для тома
    """
    conn = await get_db_connection()
    query = f"""
    INSERT INTO {TABLE_NAME} (volume_id, file_path, number)
    VALUES ($1, $2, $3)
    RETURNING id, file_path
    """
    new_file = await conn.fetchrow(query, volume_id, file_path, number)
    await conn.close()
    return new_file