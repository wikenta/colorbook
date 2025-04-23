--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: studio; Type: TABLE DATA; Schema: cartoons; Owner: coloring_admin_user
--



--
-- Data for Name: cartoon; Type: TABLE DATA; Schema: cartoons; Owner: coloring_admin_user
--



--
-- Data for Name: person; Type: TABLE DATA; Schema: cartoons; Owner: coloring_admin_user
--



--
-- Data for Name: picture; Type: TABLE DATA; Schema: coloring; Owner: coloring_admin_user
--



--
-- Data for Name: character_on_page; Type: TABLE DATA; Schema: coloring; Owner: coloring_admin_user
--



--
-- Data for Name: publisher; Type: TABLE DATA; Schema: coloring; Owner: coloring_admin_user
--

INSERT INTO coloring.publisher VALUES ('69cd0959-d70d-46d1-8413-dc4077165bf9', 'Hachette', 'Hachette');
INSERT INTO coloring.publisher VALUES ('e8594798-61cb-4a0f-9342-f5f88b74cda8', 'Dessain et Tolra', 'Dessain et Tolra');


--
-- Data for Name: series; Type: TABLE DATA; Schema: coloring; Owner: coloring_admin_user
--

INSERT INTO coloring.series VALUES ('4192d963-ecda-4268-a1d1-e6b50d7a7d22', '69cd0959-d70d-46d1-8413-dc4077165bf9', NULL, NULL, 'Coloriages mystères', 'Coloriages mystères');
INSERT INTO coloring.series VALUES ('6d7d6637-9519-43f6-addd-17f0f9d94cac', '69cd0959-d70d-46d1-8413-dc4077165bf9', '4192d963-ecda-4268-a1d1-e6b50d7a7d22', ' ', 'Disney', 'Дисней');
INSERT INTO coloring.series VALUES ('50c2bacf-5a7a-48bc-8866-a470d80cb918', '69cd0959-d70d-46d1-8413-dc4077165bf9', '6d7d6637-9519-43f6-addd-17f0f9d94cac', ' — ', 'Best of', 'Лучшее');
INSERT INTO coloring.series VALUES ('b35f9342-7fbc-48d3-98f0-9a305b6e4ada', '69cd0959-d70d-46d1-8413-dc4077165bf9', '6d7d6637-9519-43f6-addd-17f0f9d94cac', ' — ', 'Les Grands classiques', 'Великая классика');
INSERT INTO coloring.series VALUES ('5201f65d-900c-41b8-8133-0f2a2635fc38', '69cd0959-d70d-46d1-8413-dc4077165bf9', '4192d963-ecda-4268-a1d1-e6b50d7a7d22', ' — ', 'Looney Tunes', 'Looney Tunes');
INSERT INTO coloring.series VALUES ('bb06bd39-24c2-4c42-a301-b5aad6d48de8', '69cd0959-d70d-46d1-8413-dc4077165bf9', '4192d963-ecda-4268-a1d1-e6b50d7a7d22', ' — ', 'Pixar', 'Pixar');
INSERT INTO coloring.series VALUES ('7abb30a2-2a04-4136-8718-5d8d4256fa64', '69cd0959-d70d-46d1-8413-dc4077165bf9', NULL, ' ', 'Grand bloc', 'Grand bloc');
INSERT INTO coloring.series VALUES ('ef4bfa8b-1918-4ae2-916e-26a2a8aa8054', '69cd0959-d70d-46d1-8413-dc4077165bf9', '7abb30a2-2a04-4136-8718-5d8d4256fa64', ' — ', 'Trompe l''œil', 'Trompe l''œil');
INSERT INTO coloring.series VALUES ('13fffaf3-ac6b-48f8-bf26-47c5912fbe93', '69cd0959-d70d-46d1-8413-dc4077165bf9', '6d7d6637-9519-43f6-addd-17f0f9d94cac', ' — ', 'Trompe l''œil', 'Trompe l''œil');
INSERT INTO coloring.series VALUES ('e3e3c76e-1e26-4d79-a73f-715558cf7590', '69cd0959-d70d-46d1-8413-dc4077165bf9', NULL, ' ', 'Colorea y descubre el misterio', 'Раскрась и открой тайну');
INSERT INTO coloring.series VALUES ('ac2f6bd5-7365-44f6-8d6b-7fb6afdce411', '69cd0959-d70d-46d1-8413-dc4077165bf9', 'e3e3c76e-1e26-4d79-a73f-715558cf7590', ' ', 'Disney', 'Дисней');
INSERT INTO coloring.series VALUES ('080bcede-c08d-4500-b21a-bef07ae77ff5', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', NULL, ' ', '40 coloriages mystère', '40 загадочных раскрасок');


--
-- Data for Name: volume; Type: TABLE DATA; Schema: coloring; Owner: coloring_admin_user
--

INSERT INTO coloring.volume VALUES ('fa09f243-c698-4357-b69c-471266f21b2e', '69cd0959-d70d-46d1-8413-dc4077165bf9', 'bb06bd39-24c2-4c42-a301-b5aad6d48de8', ' ', 2020, 100, 'Tome 1', 'Том 1');
INSERT INTO coloring.volume VALUES ('eddc866e-ca0f-4d12-b272-a9bdcfd4876d', '69cd0959-d70d-46d1-8413-dc4077165bf9', 'bb06bd39-24c2-4c42-a301-b5aad6d48de8', ' ', 2020, 100, 'Tome 2', 'Том 2');
INSERT INTO coloring.volume VALUES ('1e17dd02-7702-48c4-bbcf-bc2ffe6abfbb', '69cd0959-d70d-46d1-8413-dc4077165bf9', '4192d963-ecda-4268-a1d1-e6b50d7a7d22', ' — ', 2024, 50, 'Barbie', 'Барби');
INSERT INTO coloring.volume VALUES ('5d34eddd-4bd3-457e-9159-7a5f3e12ae00', '69cd0959-d70d-46d1-8413-dc4077165bf9', '4192d963-ecda-4268-a1d1-e6b50d7a7d22', ' — ', 2024, 100, 'Schtroumpfs', 'Смурфики');
INSERT INTO coloring.volume VALUES ('68d8bfd7-346b-47fa-b78d-89e9bd0106fb', '69cd0959-d70d-46d1-8413-dc4077165bf9', '5201f65d-900c-41b8-8133-0f2a2635fc38', ' ', 2022, 100, 'Tome 1', 'Том 1');
INSERT INTO coloring.volume VALUES ('3484b336-fcdf-4778-acc6-66b66e42ab3b', '69cd0959-d70d-46d1-8413-dc4077165bf9', '5201f65d-900c-41b8-8133-0f2a2635fc38', ' ', 2023, 100, 'Tome 2', 'Том 2');
INSERT INTO coloring.volume VALUES ('4c09cfdd-d586-4112-8aa9-503770a5f045', '69cd0959-d70d-46d1-8413-dc4077165bf9', '5201f65d-900c-41b8-8133-0f2a2635fc38', ' ', 2024, 100, 'Tome 3', 'Том 3');
INSERT INTO coloring.volume VALUES ('381aa1a4-a4f2-4d85-8857-8864c3d0b01d', '69cd0959-d70d-46d1-8413-dc4077165bf9', 'ef4bfa8b-1918-4ae2-916e-26a2a8aa8054', ' ', 2021, 50, 'Tome 1', 'Том 1');
INSERT INTO coloring.volume VALUES ('1eaa6afd-bf0e-4d1e-8cd6-a5063f9fa570', '69cd0959-d70d-46d1-8413-dc4077165bf9', 'ef4bfa8b-1918-4ae2-916e-26a2a8aa8054', ' ', 2023, 36, 'Tome 2', 'Том 2');
INSERT INTO coloring.volume VALUES ('d4b896eb-c20a-4feb-a0ec-3b85e39e4141', '69cd0959-d70d-46d1-8413-dc4077165bf9', '13fffaf3-ac6b-48f8-bf26-47c5912fbe93', ' ', 2018, 100, 'Tome 1', 'Том 1');
INSERT INTO coloring.volume VALUES ('43ab9891-97c6-47ec-bb60-17718dfd0dd5', '69cd0959-d70d-46d1-8413-dc4077165bf9', '13fffaf3-ac6b-48f8-bf26-47c5912fbe93', ' ', 2024, 100, 'Babies', 'Дети');
INSERT INTO coloring.volume VALUES ('221acb2d-96e2-4d2d-815a-6ed9d36614a3', '69cd0959-d70d-46d1-8413-dc4077165bf9', '13fffaf3-ac6b-48f8-bf26-47c5912fbe93', ' ', 2023, 100, 'Héros vs Méchants', 'Герои и злодеи');
INSERT INTO coloring.volume VALUES ('91891bff-d4f6-4967-9f51-900fcf1056f0', '69cd0959-d70d-46d1-8413-dc4077165bf9', '13fffaf3-ac6b-48f8-bf26-47c5912fbe93', ' ', 2019, 100, 'Tome 2', 'Том 2');
INSERT INTO coloring.volume VALUES ('8b4afad7-e05f-4719-b574-f130d499279b', '69cd0959-d70d-46d1-8413-dc4077165bf9', '13fffaf3-ac6b-48f8-bf26-47c5912fbe93', ' ', 2021, 100, 'Tome 3', 'Том 3');
INSERT INTO coloring.volume VALUES ('1eb92937-69cf-40ef-8f00-9ce20b39225c', '69cd0959-d70d-46d1-8413-dc4077165bf9', '4192d963-ecda-4268-a1d1-e6b50d7a7d22', ' — ', 2024, 100, 'L''Âge de glace', 'Ледниковый период');
INSERT INTO coloring.volume VALUES ('0102e610-6685-455f-9185-56752cba9fe9', '69cd0959-d70d-46d1-8413-dc4077165bf9', '6d7d6637-9519-43f6-addd-17f0f9d94cac', ' — ', 2022, 100, 'Bestiaire', 'Бестиарий');
INSERT INTO coloring.volume VALUES ('6cb018a6-0493-439b-ac67-a7feabde36cc', '69cd0959-d70d-46d1-8413-dc4077165bf9', '50c2bacf-5a7a-48bc-8866-a470d80cb918', ' ', 2023, 100, 'Bestiaire', 'Бестиарий');
INSERT INTO coloring.volume VALUES ('fc4fe2ea-6851-4fac-9b13-3ab4b06317b9', '69cd0959-d70d-46d1-8413-dc4077165bf9', '6d7d6637-9519-43f6-addd-17f0f9d94cac', ' — ', 2020, 100, 'Chiots et chiens', 'Щенки и собаки');
INSERT INTO coloring.volume VALUES ('f2bf4c53-380e-422b-bb42-03265a9d6e54', '69cd0959-d70d-46d1-8413-dc4077165bf9', '6d7d6637-9519-43f6-addd-17f0f9d94cac', ' — ', 2024, 100, 'Petites bêtes', 'Маленькие существа');
INSERT INTO coloring.volume VALUES ('f073f0c6-055a-4e7e-a1c4-9ef3700afade', '69cd0959-d70d-46d1-8413-dc4077165bf9', 'ac2f6bd5-7365-44f6-8d6b-7fb6afdce411', '. ', 2019, 100, 'Felinos', 'Кошки');
INSERT INTO coloring.volume VALUES ('a767cf4e-aec5-43a3-8db6-cb15bca661da', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2024, 40, 'Au fil des saisons', 'В ритме времён года');
INSERT INTO coloring.volume VALUES ('b6644301-3fe6-4563-87f8-2cf8ae77ad91', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2024, 40, 'Fleurs et bouquets', 'Цветы и букеты');
INSERT INTO coloring.volume VALUES ('b6b9ae59-bd33-4ff6-925f-f048b67ff176', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2025, 40, 'Dolce vita', 'Сладкая жизнь');
INSERT INTO coloring.volume VALUES ('923ccc5d-29e9-49f7-a7ac-191870c27488', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2025, 40, 'Week-end à la campagne', 'Выходные в деревне');
INSERT INTO coloring.volume VALUES ('c369a62e-ce42-4784-9c89-165fde5a1e0f', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2025, 40, 'Tour de France', 'Путешествие по Франции');
INSERT INTO coloring.volume VALUES ('a75d3136-573d-437a-87c1-c6e1bf62e64b', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2023, 40, 'Merveilleux voyages', 'Удивительные путешествия');
INSERT INTO coloring.volume VALUES ('2659055d-382b-43bc-8e8c-85c24aa2c2d6', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2025, 40, 'Affiches rétros', 'Ретро-афиши');
INSERT INTO coloring.volume VALUES ('dd965a44-62a9-455e-8716-68721d88dd3f', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2023, 40, 'Incroyable nature', 'Невероятная природа');
INSERT INTO coloring.volume VALUES ('cedc5527-583a-4f17-a230-c5ebf7ec0ca0', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2025, 40, 'Incroyables années folles', 'Ревущие двадцатые');
INSERT INTO coloring.volume VALUES ('a64f0ed4-4638-452c-a323-86fea57ff806', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2024, 40, 'Merveilleux animaux', 'Удивительные животные');
INSERT INTO coloring.volume VALUES ('29e3b8c1-acc5-434f-96ce-196256514606', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2025, 40, 'Parcs nationaux américains', 'Национальные парки Америки');
INSERT INTO coloring.volume VALUES ('3af7948a-9203-4c9a-88e7-a230202b276f', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2025, 40, 'Blasons américains', 'Американские гербы');
INSERT INTO coloring.volume VALUES ('329b3aa9-172c-451b-8273-ec284af9ad7e', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2024, 40, 'Univers mangas', 'Мир манги');
INSERT INTO coloring.volume VALUES ('2f6ab1a9-8648-4f53-8236-eea1025c9159', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2024, 40, 'Esprit Mandalas', 'Дух мандал');
INSERT INTO coloring.volume VALUES ('8b3165eb-4d51-445f-ab33-9990f51fe9b2', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2024, 40, 'Le pouvoir des sorcières', 'Сила ведьм');
INSERT INTO coloring.volume VALUES ('37a02c70-fb23-47cc-ae03-c310093c2a46', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2023, 40, 'Énergies & divination', 'Энергии и прорицание');
INSERT INTO coloring.volume VALUES ('fab11509-367d-4dc1-93d1-255d50876523', 'e8594798-61cb-4a0f-9342-f5f88b74cda8', '080bcede-c08d-4500-b21a-bef07ae77ff5', ' ', 2025, 40, 'Merveilleux Japon', 'Удивительная Япония');


--
-- Data for Name: page; Type: TABLE DATA; Schema: coloring; Owner: coloring_admin_user
--



--
-- Data for Name: coloring_file; Type: TABLE DATA; Schema: files; Owner: coloring_admin_user
--



--
-- Data for Name: cover_file; Type: TABLE DATA; Schema: files; Owner: coloring_admin_user
--



--
-- Data for Name: page_file; Type: TABLE DATA; Schema: files; Owner: coloring_admin_user
--



--
-- Data for Name: solution_file; Type: TABLE DATA; Schema: files; Owner: coloring_admin_user
--



--
-- PostgreSQL database dump complete
--

