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

echo "[1/4] Обновление версии из pyproject.toml..."
python3 "$(dirname "$0")/update_version.py"
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось обновить версию"
    exit 1
fi

echo "[2/4] Синхронизация зависимостей (включая dev)..."
uv sync --dev
if [ $? -ne 0 ]; then
    echo "ОШИБКА: Не удалось синхронизировать зависимости"
    exit 1
fi

echo "[3/4] Создание исполняемого файла..."
uv run pyinstaller build_scripts/test_suite_executor.spec --clean
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