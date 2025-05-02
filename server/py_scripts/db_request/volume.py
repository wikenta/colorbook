from asyncpg import Record
from typing import Optional, List
from db_request.db_connect import get_db_connection

async def get_all_books() -> List[Record]:
    """
    Все книги: id, release_year, page_count, name_en, name_ru, full_name_en и full_name_ru, publisher_id
    """
    conn = await get_db_connection()
    query = """
    SELECT v.id, v.release_year, v.page_count, v.name_en, v.name_ru, vn.full_name_en, vn.full_name_ru, v.publisher_id
    FROM coloring.volume v
    JOIN coloring.volume_full_name vn ON v.id = vn.id
    ORDER BY vn.full_name_ru
    """
    books = await conn.fetch(query)
    await conn.close()
    return books

async def get_books_by_publisher(publisher_id: str) -> List[Record]:
    """
    Все книги по ID издателя: id, release_year, page_count, name_en, name_ru, full_name_en и full_name_ru, publisher_id
    """
    conn = await get_db_connection()
    query = """
    SELECT v.id, v.release_year, v.page_count, v.name_en, v.name_ru, vn.full_name_en, vn.full_name_ru, v.publisher_id
    FROM coloring.volume v
    JOIN coloring.volume_full_name vn ON v.id = vn.id
    WHERE v.publisher_id = $1
    ORDER BY vn.full_name_ru
    """
    books = await conn.fetch(query, publisher_id)
    await conn.close()
    return books

async def get_books_by_publisher_without_series(publisher_id: str) -> List[Record]:
    """
    Все книги по ID издателя без серий: id, release_year, page_count, name_en, name_ru, full_name_en и full_name_ru, publisher_id
    """
    conn = await get_db_connection()
    query = """
    SELECT v.id, v.release_year, v.page_count, v.name_en, v.name_ru, vn.full_name_en, vn.full_name_ru, v.publisher_id
    FROM coloring.volume v
    JOIN coloring.volume_full_name vn ON v.id = vn.id
    WHERE v.publisher_id = $1 AND v.series_id IS NULL
    ORDER BY vn.full_name_ru
    """
    books = await conn.fetch(query, publisher_id)
    await conn.close()
    return books

async def get_books_by_series(series_id: str) -> List[Record]:
    """
    Все книги по ID серии: id, release_year, page_count, name_en, name_ru, full_name_en и full_name_ru, publisher_id
    """
    conn = await get_db_connection()
    query = """
    SELECT v.id, v.release_year, v.page_count, v.name_en, v.name_ru, vn.full_name_en, vn.full_name_ru, v.publisher_id
    FROM coloring.volume v
    JOIN coloring.volume_full_name vn ON v.id = vn.id
    WHERE v.series_id = $1
    ORDER BY vn.full_name_ru
    """
    books = await conn.fetch(query, series_id)
    await conn.close()
    return books

async def get_book_by_id(book_id: str) -> Optional[Record]:
    """
    Книга по ID: id, release_year, page_count, name_en, name_ru, full_name_en и full_name_ru, publisher_id
    """
    conn = await get_db_connection()
    query = """
    SELECT v.id, v.release_year, v.page_count, v.name_en, v.name_ru, vn.full_name_en, vn.full_name_ru, v.publisher_id
    FROM coloring.volume v
    JOIN coloring.volume_full_name vn ON v.id = vn.id
    WHERE v.id = $1
    """
    book = await conn.fetchrow(query, book_id)
    await conn.close()
    return book

async def get_all_books_in_series(series_id: str) -> List[Record]:
    """
    Все книги в серии: id, release_year, page_count, name_en, name_ru, full_name_en и full_name_ru, publisher_id
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
    SELECT v.id, v.release_year, v.page_count, v.name_en, v.name_ru, vn.full_name_en, vn.full_name_ru, v.publisher_id
    FROM series_tree st
    JOIN coloring.volume v ON v.series_id = st.id
    JOIN coloring.volume_full_name vn ON v.id = vn.id
    ORDER BY vn.full_name_ru
    """
    books = await conn.fetch(query, series_id)
    await conn.close()
    return books