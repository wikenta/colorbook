import psycopg2  # Импортируем библиотеку для работы с PostgreSQL
from secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Подключение к базе данных
connection = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT)

# Создание курсора
cursor = connection.cursor()

# Пример 1: Чтение всех строк из таблицы (предположим, что у тебя есть таблица "pdf_files")
cursor.execute("SELECT * FROM books;")
rows = cursor.fetchall()  # Получаем все строки из результата

# Выводим все строки
for row in rows:
    print(row)

# Пример 2: Запись строки в таблицу
cursor.execute("""
    INSERT INTO books (name)
    VALUES (%s);
""", ('название книги',))  # Замените 'название книги' на нужное значение

# Подтверждаем изменения в базе данных
connection.commit()

# Закрытие курсора и соединения
cursor.close()
connection.close()
