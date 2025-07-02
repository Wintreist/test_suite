#!/bin/bash
# Скрипт для сборки test-suite-executor в Linux executable

set -e

echo "Сборка test-suite-executor для Linux..."

# Активируем виртуальное окружение если есть
if [ -f ".venv/bin/activate" ]; then
    echo "Активируем виртуальное окружение..."
    source .venv/bin/activate
else
    echo "Виртуальное окружение не найдено, создаем..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Устанавливаем зависимости для сборки
echo "Устанавливаем зависимости для сборки..."
pip install -e .[build]

# Создаем директорию для сборки
mkdir -p dist
mkdir -p build

# Запускаем PyInstaller
echo "Запускаем PyInstaller..."
pyinstaller test_suite_executor.spec --clean --noconfirm

# Переименовываем исполняемый файл и делаем его исполняемым
if [ -f "dist/test-suite-executor" ]; then
    chmod +x dist/test-suite-executor
    echo "Сборка завершена успешно!"
    echo "Исполняемый файл: dist/test-suite-executor"
else
    echo "Ошибка сборки!"
    exit 1
fi