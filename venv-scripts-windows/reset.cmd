@echo off
chcp 65001 > nul
echo [СТАРТ] Сброс виртуального окружения

if exist venv (
    echo Удаляю существующий venv...
    rmdir /s /q venv
    if exist venv (
        echo [ОШИБКА] Не удалось удалить существующий venv
        exit /b 1
    )
    echo [v] Существующий venv удалён
)
if exist requirements.txt (
    echo Удаляю файл requirements.txt...
    del requirements.txt
    if exist requirements.txt (
        echo [ОШИБКА] Не удалось удалить requirements.txt
        exit /b 1
    )
    echo [v] Файл requirements.txt удалён
)

echo Создаю новый venv...
python -m venv venv
if not exist venv (
    echo [ОШИБКА] Не удалось создать venv
    exit /b 1
)
echo [v] Новый venv создан

echo Устанавливаю базовые зависимости из requirements-base.txt...
if exist requirements-base.txt (
    venv\Scripts\pip.exe install -r requirements-base.txt
) else (
    echo [ОШИБКА] Файл базовых зависимостей requirements-base.txt не найден
    exit /b 1
)
echo.
echo [v] Установлены зависимости

echo Сохраняю текущие зависимости в requirements.txt...
venv\Scripts\pip.exe freeze > requirements.txt
if not exist requirements.txt (
    echo [ОШИБКА] Не удалось создать requirements.txt
    exit /b 1
)
echo [v] Файл requirements.txt сохранен

echo [УСПЕХ] Виртуальное окружение успешно сброшено и обновлено