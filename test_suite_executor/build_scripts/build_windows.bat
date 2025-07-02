@echo off
REM Скрипт для сборки test-suite-executor в Windows executable
echo Сборка test-suite-executor для Windows...

REM Активируем виртуальное окружение если есть
if exist ".venv\Scripts\activate.bat" (
    echo Активируем виртуальное окружение...
    call .venv\Scripts\activate.bat
) else (
    echo Виртуальное окружение не найдено, создаем...
    python -m venv .venv
    call .venv\Scripts\activate.bat
)

REM Устанавливаем зависимости для сборки
echo Устанавливаем зависимости для сборки...
pip install -e .[build]

REM Создаем директорию для сборки
if not exist "dist" mkdir dist
if not exist "build" mkdir build

REM Запускаем PyInstaller
echo Запускаем PyInstaller...
pyinstaller test_suite_executor.spec --clean --noconfirm

REM Переименовываем исполняемый файл
if exist "dist\test-suite-executor.exe" (
    echo Сборка завершена успешно!
    echo Исполняемый файл: dist\test-suite-executor.exe
) else (
    echo Ошибка сборки!
    exit /b 1
)

pause