#!/bin/bash

echo "========================================"
echo "  Сборка test-suite-executor для Linux"
echo "========================================"

# Проверяем наличие uv
if ! command -v uv &> /dev/null; then
    echo "ОШИБКА: uv не установлен. Установите uv сначала."
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "[1/4] Синхронизация зависимостей..."
uv sync
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось синхронизировать зависимости"
    exit 1
fi

echo "[2/4] Установка PyInstaller..."
uv add pyinstaller
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось установить PyInstaller"
    exit 1
fi

echo "[3/4] Создание исполняемого файла..."
uv run pyinstaller test_suite_executor.spec --clean
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось создать исполняемый файл"
    exit 1
fi

echo "[4/4] Проверка результата..."
if [ -f "dist/test-suite-executor" ]; then
    echo "✅ Успешно создан: dist/test-suite-executor"
    ls -la dist/test-suite-executor
    echo "Делаем файл исполняемым..."
    chmod +x dist/test-suite-executor
else
    echo "❌ Файл не был создан"
    exit 1
fi

echo ""
echo "========================================"
echo "   Сборка завершена успешно!"
echo "========================================"
echo "Исполняемый файл: dist/test-suite-executor"
echo ""