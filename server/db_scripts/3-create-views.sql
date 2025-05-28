CREATE OR REPLACE VIEW coloring.series_full_name AS
WITH RECURSIVE series_chain(id, full_name_en, full_name_ru) AS (
    SELECT id, name_en, name_ru
    FROM coloring.series
    WHERE parent_series_id IS NULL

    UNION ALL

    SELECT s.id,
           sc.full_name_en || s.parent_name_separator || s.name_en,
           sc.full_name_ru || s.parent_name_separator || s.name_ru
    FROM coloring.series s
    JOIN series_chain sc ON s.parent_series_id = sc.id
)
SELECT * FROM series_chain;

CREATE OR REPLACE VIEW coloring.volume_full_name AS
SELECT
    v.id,
    COALESCE(s.full_name_en || v.series_name_separator || v.name_en, v.name_en) AS full_name_en,
    COALESCE(s.full_name_ru || v.series_name_separator || v.name_ru, v.name_ru) AS full_name_ru
FROM coloring.volume v
LEFT JOIN coloring.series_full_name s ON v.series_id = s.id;
