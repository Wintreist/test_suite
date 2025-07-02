# Добавлена поддержка сборки в исполняемые файлы

## Что добавлено

В проект `test_suite_executor` добавлена возможность сборки в standalone исполняемые файлы для Windows (.exe) и Linux (bin).

### Новые файлы:

1. **`main.py`** - точка входа для PyInstaller
2. **`test_suite_executor.spec`** - конфигурация PyInstaller для сборки
3. **`build_scripts/build_windows.bat`** - скрипт сборки для Windows
4. **`build_scripts/build_linux.sh`** - скрипт сборки для Linux
5. **`Makefile`** - автоматизация процесса сборки
6. **`BUILD.md`** - подробная документация по сборке
7. **`test_executable.py`** - скрипт тестирования собранного исполняемого файла
8. **`.gitignore`** - исключение файлов сборки из Git

### Обновленные файлы:

1. **`pyproject.toml`** - добавлены зависимости для сборки и entry point

## Быстрый старт

```bash
# Перейти в директорию проекта
cd test_suite_executor

# Автоматическая настройка и сборка
make setup
make build

# Тестирование собранного файла
make test-executable
```

## Результат

После сборки в директории `dist/` будет создан исполняемый файл:
- **Linux**: `test-suite-executor`
- **Windows**: `test-suite-executor.exe`

Исполняемый файл запускает FastAPI сервер на порту 8888 (по умолчанию) и предоставляет API для запуска тестовых наборов.

## Использование

```bash
# Linux
./dist/test-suite-executor

# Windows
dist\test-suite-executor.exe

# С настройкой порта
ExecutorSettings__port=9999 ./dist/test-suite-executor
```

Сервер будет доступен по адресу `http://localhost:8888` (или указанному порту).

## Преимущества

- ✅ Standalone файлы - не требуют установки Python
- ✅ Кроссплатформенность - Windows и Linux
- ✅ Автоматизированная сборка через Makefile
- ✅ Тестирование собранных файлов
- ✅ Настройка через переменные окружения
- ✅ Полная документация процесса сборки