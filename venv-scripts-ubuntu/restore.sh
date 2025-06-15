#!/bin/bash

echo "[СТАРТ] Восстановление виртуального окружения"

if [ -d "venv" ]; then
    echo "Удаляю существующий venv..."
    rm -rf venv
    if [ -d "venv" ]; then
        echo "[ОШИБКА] Не удалось удалить существующий venv"
        exit 1
    fi
    echo "[v] Существующий venv удалён"
fi

echo "Создаю новый venv..."
python3 -m venv venv
if [ ! -d "venv" ]; then
    echo "[ОШИБКА] Не удалось создать venv"
    exit 1
fi
echo "[v] Новый venv создан"

echo "Устанавливаю зависимости из requirements.txt..."
if [ -f "requirements.txt" ]; then
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "[ОШИБКА] Файл зависимостей requirements.txt не найден"
    exit 1
fi

echo
echo "[v] Установлены зависимости"

echo "Сохраняю текущие зависимости в requirements.txt..."
pip freeze > requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "[ОШИБКА] Не удалось записать requirements.txt"
    exit 1
fi
echo "[v] Файл requirements.txt сохранен"

echo "[УСПЕХ] Виртуальное окружение успешно восстановлено"
