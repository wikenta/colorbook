#!/bin/bash

# 🐍 Проверка и создание виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создаём виртуальное окружение..."
    python3 -m venv venv
fi

# 🏁 Активируем виртуальное окружение
source venv/bin/activate

# 📄 Устанавливаем зависимости из requirements.txt, если он есть
if [ -f "requirements.txt" ]; then
    echo "📚 requirements.txt найден – устанавливаем зависимости..."
    pip install -r requirements.txt
else
    echo "🆕 requirements.txt не найден – устанавливаем базовые пакеты..."
    pip install asyncpg aiogram

    echo "📝 Сохраняем зависимости в requirements.txt..."
    pip freeze > requirements.txt
    echo "🎯 requirements.txt создан!"
fi

# 🏁 Готово!
echo "✅ Всё готово! Кодим с кайфом ✨"
