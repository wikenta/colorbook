-- Убедись, что расширение uuid-ossp или pgcrypto включено
-- Это нужно только один раз
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Схема: Мультфильмы
CREATE SCHEMA IF NOT EXISTS cartoons;

-- Таблица: Студия мультипликации
CREATE TABLE IF NOT EXISTS cartoons.studio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Имя студии уникально
    name_en TEXT NOT NULL UNIQUE,
    name_ru TEXT NOT NULL UNIQUE
);

-- Таблица: Мультфильм
CREATE TABLE IF NOT EXISTS cartoons.cartoon (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    studio_id UUID NOT NULL REFERENCES cartoons.studio(id) ON DELETE NO ACTION,
    release_year INTEGER NOT NULL CHECK (release_year BETWEEN 1800 AND 2100),
    -- Название мультфильма уникально в пределах студии
    name_en TEXT NOT NULL,
    name_ru TEXT NOT NULL,
    UNIQUE (studio_id, name_en),
    UNIQUE (studio_id, name_ru)
);

-- Таблица: Персонаж
CREATE TABLE IF NOT EXISTS cartoons.person (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cartoon_id UUID NOT NULL REFERENCES cartoons.cartoon(id) ON DELETE NO ACTION,
    -- Имя персонажа уникально в пределах мультфильма
    name_en TEXT NOT NULL,
    name_ru TEXT NOT NULL,
    UNIQUE (cartoon_id, name_en),
    UNIQUE (cartoon_id, name_ru)
);

-- Схема: Раскраски
CREATE SCHEMA IF NOT EXISTS coloring;

-- Таблица: Издатель раскрасок
CREATE TABLE IF NOT EXISTS coloring.publisher (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Название издателя уникально
    name_en TEXT NOT NULL UNIQUE,
    name_ru TEXT NOT NULL UNIQUE
);

-- Таблица: Серия раскрасок
CREATE TABLE IF NOT EXISTS coloring.series (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    publisher_id UUID NOT NULL REFERENCES coloring.publisher(id) ON DELETE NO ACTION,
    -- Родительская серия
    parent_series_id UUID REFERENCES coloring.series(id) ON DELETE NO ACTION,
    -- Разделитель между названиями родительской серии и текущей
    parent_name_separator TEXT DEFAULT ' ',
    -- Название серии уникально в пределах родительской серии и издателя
    name_en TEXT NOT NULL,
    name_ru TEXT NOT NULL,
    UNIQUE (publisher_id, parent_series_id, name_en),
    UNIQUE (publisher_id, parent_series_id, name_ru)
);

-- Таблица: Том (книга) раскрасок
CREATE TABLE IF NOT EXISTS coloring.volume (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Проверяется, что publisher_id совпадает с coloring_series.publisher_id
    publisher_id UUID NOT NULL REFERENCES coloring.publisher(id) ON DELETE NO ACTION,
    -- Серия может быть NULL, если это отдельный том
    series_id UUID REFERENCES coloring.series(id) ON DELETE NO ACTION,
    -- Разделитель между названиями серии и тома
    series_name_separator TEXT DEFAULT ' ',
    release_year INTEGER NOT NULL CHECK (release_year BETWEEN 1800 AND 2100),
    page_count INTEGER NOT NULL CHECK (page_count > 0),
    -- Название тома уникально в пределах серии, издателя и года выпуска
    name_en TEXT NOT NULL,
    name_ru TEXT NOT NULL,
    UNIQUE (publisher_id, series_id, name_en, release_year),
    UNIQUE (publisher_id, series_id, name_ru, release_year)
);

-- Таблица: Картина (может встречаться в нескольких томах)
CREATE TABLE IF NOT EXISTS coloring.picture (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);

-- Таблица: Страница с картиной
CREATE TABLE IF NOT EXISTS coloring.page (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    volume_id UUID NOT NULL REFERENCES coloring.volume(id) ON DELETE NO ACTION,
    -- Номер страницы уникален в пределах тома, не превышает coloring_volume.page_count
    page_number INTEGER NOT NULL CHECK (page_number > 0),
    -- Картина может располагаться на нескольких страницах
    picture_id UUID NOT NULL REFERENCES coloring.picture(id) ON DELETE NO ACTION,
    -- В решениях может быть подпись под страницей
    name_en TEXT,
    name_ru TEXT,
    UNIQUE (volume_id, page_number)
);

-- Таблица: Персонаж на картине (не повторяется на одной картине)
CREATE TABLE IF NOT EXISTS coloring.character_on_page (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    picture_id UUID NOT NULL REFERENCES coloring.picture(id) ON DELETE NO ACTION,
    person_id UUID NOT NULL REFERENCES cartoons.person(id) ON DELETE NO ACTION,
    UNIQUE (picture_id, person_id)
);

-- Схема: Файлы
CREATE SCHEMA IF NOT EXISTS files;

-- Таблица: Файл раскраски
CREATE TABLE IF NOT EXISTS files.volume_file (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    volume_id UUID NOT NULL REFERENCES coloring.volume(id) ON DELETE NO ACTION,
    file_path TEXT NOT NULL,  -- Путь к файлу на диске
    file_hash TEXT NOT NULL,  -- Хеш файла (например, SHA-256)
    min_dpi INTEGER NOT NULL CHECK (min_dpi >= 0),  -- Минимальное разрешение в файле, до обработки = 0
    max_dpi INTEGER NOT NULL CHECK (max_dpi >= min_dpi),  -- Максимальное разрешение в файле
    UNIQUE (volume_id, file_hash)  -- Хеш уникален в пределах тома
);

-- Таблица: Файл обложки
CREATE TABLE IF NOT EXISTS files.cover_file (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    volume_id UUID NOT NULL REFERENCES coloring.volume(id) ON DELETE NO ACTION,
    file_path TEXT NOT NULL,  -- Путь к файлу на диске
    file_hash TEXT NOT NULL,  -- Хеш файла (например, SHA-256)
    dpi INTEGER NOT NULL CHECK (dpi >= 0),  -- Разрешение, до обработки = 0
    UNIQUE (volume_id, file_hash)  -- Хеш уникален в пределах файлов обложки
);

-- Таблица: Файл картины
CREATE TABLE IF NOT EXISTS files.picture_file (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    picture_id UUID NOT NULL REFERENCES coloring.picture(id) ON DELETE NO ACTION,
    file_path TEXT NOT NULL,  -- Путь к файлу на диске
    file_hash TEXT NOT NULL,  -- Хеш файла (например, SHA-256)
    dpi INTEGER NOT NULL CHECK (dpi >= 0),  -- Разрешение, до обработки = 0
    UNIQUE (picture_id, file_hash)  -- Хеш уникален в пределах файлов картины
);

-- Таблица: Файл решения
CREATE TABLE IF NOT EXISTS files.solution_file (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    picture_id UUID NOT NULL REFERENCES coloring.picture(id) ON DELETE NO ACTION,
    file_path TEXT NOT NULL,  -- Путь к файлу на диске
    file_hash TEXT NOT NULL,  -- Хеш файла (например, SHA-256)
    dpi INTEGER NOT NULL CHECK (dpi >= 0),  -- Разрешение, до обработки = 0
    UNIQUE (picture_id, file_hash)  -- Хеш уникален в пределах файлов решения картины
);

-- Таблица: Файл готовой работы
CREATE TABLE IF NOT EXISTS files.colored_file (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    picture_id UUID NOT NULL REFERENCES coloring.picture(id) ON DELETE NO ACTION,
    comment TEXT,  -- автор работы, дата и пр, пока без уточнения
    file_path TEXT NOT NULL,  -- Путь к файлу на диске
    file_hash TEXT NOT NULL,  -- Хеш файла (например, SHA-256)
    dpi INTEGER NOT NULL CHECK (dpi >= 0),  -- Разрешение, до обработки = 0
    UNIQUE (picture_id, file_hash)  -- Хеш уникален в пределах файлов картины
);