#!/bin/bash
echo "[СТАРТ] Активация виртуального окружения"

if [ ! -f "venv/bin/activate" ]; then
    echo "[ОШИБКА] Нет виртуального окружения"
    exit 1
fi

source venv/bin/activate
if [ -z "$VIRTUAL_ENV" ]; then
    echo "[ОШИБКА] Venv не активирован"
    exit 1
fi

echo "[УСПЕХ] Venv активирован: $VIRTUAL_ENV"
exit 0