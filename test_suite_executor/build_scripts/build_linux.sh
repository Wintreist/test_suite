#!/bin/bash

echo "========================================"
echo "  Сборка test-suite-executor для Linux"
echo "========================================"

# Переходим в родительскую директорию
cd "$(dirname "$0")/.."

# Проверяем наличие uv
if ! command -v uv &> /dev/null; then
    echo "ОШИБКА: uv не установлен. Установите uv сначала."
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "[1/3] Синхронизация зависимостей (включая dev)..."
uv sync --dev
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось синхронизировать зависимости"
    exit 1
fi

echo "[2/3] Создание исполняемого файла..."
uv run pyinstaller build_scripts/test_suite_executor.spec --clean
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось создать исполняемый файл"
    exit 1
fi

echo "[3/3] Проверка результата..."
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