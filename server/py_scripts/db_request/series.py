from db_request.db_connect import get_db_connection
from typing import Optional, Dict, List

async def get_series() -> List[Dict[str, str]]: 
    """
    Все серии книг: id, name_en, name_ru, full_name_en и full_name_ru
    """
    conn = await get_db_connection()
    query = """
    SELECT s.id, s.name_en. s.name_ru, sn.full_name_en, sn.full_name_ru
    FROM coloring.series s
    JOIN coloring.series_full_name sn ON s.id = sn.id
    ORDER BY s.full_name_ru
    """
    series = await conn.fetch(query)
    await conn.close()
    return series

async def get_series_by_publisher(publisher_id: str) -> List[Dict[str, str]]:
    """
    Все серии книг по ID издателя: id, name_en, name_ru, full_name_en и full_name_ru
    """
    conn = await get_db_connection()
    query = """
    SELECT s.id, s.name_en, s.name_ru, sn.full_name_en, sn.full_name_ru
    FROM coloring.series s
    JOIN coloring.series_full_name sn ON s.id = sn.id
    JOIN coloring.volume v ON v.series_id = s.id
    WHERE v.publisher_id = $1
    ORDER BY s.full_name_ru
    """
    series = await conn.fetch(query, publisher_id)
    await conn.close()
    return series

async def get_series_by_id(series_id: str) -> Optional[Dict[str, str]]:
    """
    Серия книг по ID: id, name_en, name_ru, full_name_en и full_name_ru
    """
    conn = await get_db_connection()
    query = """
    SELECT s.id, s.name_en, s.name_ru, sn.full_name_en, sn.full_name_ru
    FROM coloring.series s
    JOIN coloring.series_full_name sn ON s.id = sn.id
    WHERE s.id = $1
    """
    series = await conn.fetchrow(query, series_id)
    await conn.close()
    return series

async def get_child_series(parent_id: str) -> List[Dict[str, str]]:
    """
    Вложенные серии книг: id, name_en, name_ru, full_name_en и full_name_ru
    """
    conn = await get_db_connection()
    query = """
    SELECT s.id, s.name_en, s.name_ru, sn.full_name_en, sn.full_name_ru
    FROM coloring.series s
    JOIN coloring.series_full_name sn ON s.id = sn.id
    WHERE s.parent_series_id = $1
    ORDER BY s.full_name_ru
    """
    series = await conn.fetch(query, parent_id)
    await conn.close()
    return series

async def get_all_child_series(series_id: str) -> List[Dict[str, str]]:
    """
    Все вложенные серии книг: id, name_en, name_ru, full_name_en и full_name_ru
    """
    conn = await get_db_connection()
    query = """
    WITH RECURSIVE series_tree AS (
        SELECT id, parent_series_id
        FROM coloring.series
        WHERE id = $1

        UNION ALL

        SELECT s.id, s.parent_series_id
        FROM coloring.series s
        INNER JOIN series_tree st ON s.parent_series_id = st.id
    )
    SELECT s.id, s.name_en, s.name_ru, sn.full_name_en, sn.full_name_ru
    FROM series_tree st
    JOIN coloring.series_full_name sn ON st.id = sn.id
    ORDER BY sn.full_name_ru
    """
    series = await conn.fetch(query, series_id)
    await conn.close()
    return series

async def get_all_parent_series(series_id: str) -> List[Dict[str, str]]:
    """
    Все родительские серии книг: id, name_en, name_ru, full_name_en и full_name_ru
    """
    conn = await get_db_connection()
    query = """
    WITH RECURSIVE parent_series_tree AS (
        SELECT s.id, s.parent_series_id
        FROM coloring.series s
        WHERE s.id = $1

        UNION ALL

        SELECT s.id, s.parent_series_id
        FROM coloring.series s
        INNER JOIN parent_series_tree pst ON pst.parent_series_id = s.id
    )
    SELECT s.id, s.name_en, s.name_ru, sn.full_name_en, sn.full_name_ru
    FROM parent_series_tree pst
    JOIN coloring.series_full_name sn ON pst.id = sn.id;
    """
    series = await conn.fetch(query, series_id)
    await conn.close()
    return series