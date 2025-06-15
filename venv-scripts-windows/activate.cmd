@echo off
chcp 65001 > nul
echo [СТАРТ] Активация виртуального окружения

if not exist venv\Scripts\activate.bat (
    echo [ОШИБКА] Нет виртуального окружения
    exit /b 1
)

call venv\Scripts\activate.bat

if not defined VIRTUAL_ENV (
    echo [ОШИБКА] Venv не активирован
    exit /b 1
)
echo [УСПЕХ] Venv активирован
exit /b 0
