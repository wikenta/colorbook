-- Проверка, не ссылается ли строка на саму себя
-- Проверка согласованности и автоматическое заполнение publisher_id
CREATE OR REPLACE FUNCTION coloring.prevent_self_reference_check_and_autofill_publisher_id()
RETURNS TRIGGER AS $$
DECLARE
    cycle_check UUID;
BEGIN
    -- Проверяем, что ссылка parent_series_id не циклична
    IF NEW.parent_series_id IS NOT NULL THEN
        WITH RECURSIVE parent AS (
            SELECT id, parent_series_id
            FROM coloring.series
            WHERE id = NEW.parent_series_id
            UNION ALL
            SELECT s.id, s.parent_series_id
            FROM coloring.series s
            INNER JOIN parent p ON p.parent_series_id = s.id
        )
        SELECT id INTO cycle_check
        FROM parent
        WHERE parent_series_id = NEW.id;

        IF FOUND THEN
            RAISE EXCEPTION 'Circular reference detected in parent_series_id';
        END IF;
    END IF;

    -- Проверяем согласованность publisher_id = parent_series.publisher_id
    IF NEW.publisher_id IS NOT NULL AND NEW.parent_series_id IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1 FROM coloring.series
            WHERE id = NEW.parent_series_id AND publisher_id = NEW.publisher_id
        ) THEN
            RAISE EXCEPTION 'Series does not belong to the same publisher as the volume';
        END IF;
    END IF;

    -- Если publisher_id не указан, пишем в него parent_series.publisher_id
    IF NEW.publisher_id IS NULL AND NEW.parent_series_id IS NOT NULL THEN
        SELECT publisher_id INTO NEW.publisher_id
        FROM coloring.series
        WHERE id = NEW.parent_series_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_prevent_self_reference
BEFORE INSERT OR UPDATE ON coloring.series
FOR EACH ROW
EXECUTE FUNCTION coloring.prevent_self_reference_check_and_autofill_publisher_id();

--  Проверка согласованности и автоматическое заполнение publisher_id
CREATE OR REPLACE FUNCTION coloring.check_and_auto_fill_publisher_id()
RETURNS TRIGGER AS $$
BEGIN
    -- Проверяем согласованность publisher_id с series.publisher_id
    IF NEW.publisher_id IS NOT NULL AND NEW.series_id IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1 FROM coloring.series
            WHERE id = NEW.series_id AND publisher_id = NEW.publisher_id
        ) THEN
            RAISE EXCEPTION 'Series does not belong to the same publisher as the volume';
        END IF;
    END IF;

    -- Если publisher_id не указан, пишем в него series.publisher_id
    IF NEW.publisher_id IS NULL AND NEW.series_id IS NOT NULL THEN
        SELECT publisher_id INTO NEW.publisher_id
        FROM coloring.series
        WHERE id = NEW.series_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_volume_fill_publisher_id
BEFORE INSERT OR UPDATE ON coloring.volume
FOR EACH ROW
EXECUTE FUNCTION coloring.check_and_auto_fill_publisher_id();

-- Функция проверки, что номер страницы не превышает количество,
-- а развороты находятся на страницах, идущих подряд
CREATE OR REPLACE FUNCTION coloring.check_page_number_within_limit()
RETURNS TRIGGER AS $$
DECLARE
    max_pages INTEGER;
    page_numbers INTEGER[];
BEGIN
    -- Проверяем, что номер страницы не превышает количество страниц в томе
    SELECT page_count INTO max_pages
    FROM coloring.volume
    WHERE id = NEW.volume_id;

    IF max_pages IS NULL THEN
        RAISE EXCEPTION 'Volume not found with id: %', NEW.volume_id;
    END IF;

    IF NEW.page_number > max_pages THEN
        RAISE EXCEPTION 'Page number (got %) exceeds max page count (%) for volume %',
                        NEW.page_number, max_pages, NEW.volume_id;
    END IF;

    -- Проверяем, что страницы разворота идут подряд
    SELECT ARRAY_AGG(page_number ORDER BY page_number) INTO page_numbers
    FROM coloring.page
    WHERE picture_id = NEW.picture_id;

    IF page_numbers IS NOT NULL THEN
        -- Проверяем, что номера страниц идут подряд
        FOR i IN 1..array_length(page_numbers, 1) - 1 LOOP
            IF page_numbers[i] + 1 <> page_numbers[i + 1] THEN
                RAISE EXCEPTION 'Pages for the same picture must be consecutive';
            END IF;
        END LOOP;

        -- Проверяем, что номер страницы не совпадает с уже существующими
        IF NEW.page_number = ANY(page_numbers) THEN
            RAISE EXCEPTION 'Page number % already exists for the same picture %',
                            NEW.page_number, NEW.picture_id;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_check_page_number
BEFORE INSERT OR UPDATE ON coloring.page
FOR EACH ROW
EXECUTE FUNCTION coloring.check_page_number_within_limit();
