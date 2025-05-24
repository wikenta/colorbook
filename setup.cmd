@echo off
chcp 65001 > nul
echo ========================================
echo 🎉 Настройка виртуального окружения venv
echo ========================================

:: 1. Проверка существования venv
if not exist venv (
    echo 🚀 Создаю venv...
    python -m venv venv
) else (
    echo 👍 venv уже существует
)

:: 2. Установка зависимостей
echo 🛠️ Устанавливаю зависимости...

if exist requirements.txt (
    venv\Scripts\pip.exe install -r requirements.txt
) else (
    venv\Scripts\pip.exe install pdf2image pymupdf sqlalchemy psycopg2-binary asyncpg python-telegram-bot aiogram aiohttp cloudinary validators
)
venv\Scripts\pip.exe freeze > requirements.txt
echo 🎯 requirements.txt обновлён

:: 3. Подсказка по активации
echo.
echo 🎉 Всё готово!
echo Чтобы активировать venv, выполни:
echo.
echo     venv\Scripts\activate.bat
echo.
pause
