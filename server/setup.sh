#!/bin/bash

echo "[INFO] Запуск скрипта настройки сервера..."
sudo /bin/systemctl stop coloring-bot-dev.service

if [ -d "venv" ]; then
    echo "[CLEANUP] Удаляем старое виртуальное окружение..."
    rm -rf venv
fi

if [ -f "requirements.txt" ]; then
    echo "[CLEANUP] Удаляем старый файл зависимостей..."
    rm requirements.txt
fi

echo "[SETUP] Создаём виртуальное окружение..."
python3 -m venv venv

echo "[SETUP] Устанавливаем зависимости..."
./venv/bin/pip install asyncpg aiogram aiohttp cloudinary validators

echo "[SETUP] Сохраняем зависимости в requirements.txt..."
./venv/bin/pip freeze > requirements.txt

sudo /bin/systemctl start coloring-bot-dev.service
echo "[DONE] Настройка сервера завершена!"
