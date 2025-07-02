# Сборка test-suite-executor в исполняемые файлы

Этот документ описывает процесс сборки test-suite-executor в standalone исполняемые файлы для Windows (.exe) и Linux (bin).

## Требования

- Python 3.12+
- PyInstaller 6.0+
- Виртуальное окружение (рекомендуется)

## Быстрый старт

### Автоматическая сборка (рекомендуется)

```bash
# Настройка окружения и сборка
make setup
make build

# Или полная пересборка
make all
```

### Ручная сборка

#### Linux/macOS

```bash
# 1. Настройка окружения
python3 -m venv .venv
source .venv/bin/activate

# 2. Установка зависимостей
pip install -e .[build]

# 3. Сборка
./build_scripts/build_linux.sh
```

#### Windows

```cmd
REM 1. Настройка окружения
python -m venv .venv
.venv\Scripts\activate

REM 2. Установка зависимостей
pip install -e .[build]

REM 3. Сборка
build_scripts\build_windows.bat
```

## Результаты сборки

После успешной сборки исполняемые файлы будут находиться в директории `dist/`:

- **Linux**: `dist/test-suite-executor`
- **Windows**: `dist/test-suite-executor.exe`

## Использование исполняемых файлов

### Linux
```bash
# Запуск сервера
./dist/test-suite-executor

# Сервер будет доступен по адресу http://localhost:8888
```

### Windows
```cmd
REM Запуск сервера
dist\test-suite-executor.exe

REM Сервер будет доступен по адресу http://localhost:8888
```

## Настройка

Исполняемый файл поддерживает настройку через переменные окружения:

```bash
# Изменение порта
export ExecutorSettings__port=9999
./dist/test-suite-executor
```

## Особенности сборки

### Включенные зависимости

PyInstaller автоматически включает следующие зависимости:
- FastAPI и Uvicorn (веб-сервер)
- Pydantic (валидация данных)
- GitPython (работа с Git репозиториями)
- test-suite (основная логика тестирования)

### Размер исполняемого файла

Исполняемый файл может быть достаточно большим (50-150MB) из-за включения всех зависимостей Python и виртуальной машины.

### Время запуска

Первый запуск исполняемого файла может занять больше времени из-за распаковки временных файлов.

## Дополнительные команды Make

```bash
make help           # Показать все доступные команды
make clean          # Очистить файлы сборки
make test           # Запустить тесты
make run-dev        # Запустить в режиме разработки
make package        # Создать архив с исполняемым файлом
```

## Отладка проблем сборки

### Проблемы с зависимостями

Если PyInstaller не может найти некоторые модули, добавьте их в список `hiddenimports` в файле `test_suite_executor.spec`.

### Проблемы с путями

Убедитесь, что все относительные пути в коде корректно обрабатываются. В исполняемом файле рабочая директория может отличаться.

### Логирование

Для отладки можно включить подробное логирование PyInstaller:

```bash
pyinstaller test_suite_executor.spec --clean --noconfirm --log-level DEBUG
```

## Создание инсталлятора

### Windows (NSIS)

Для создания инсталлятора Windows можно использовать NSIS:

1. Установите NSIS
2. Создайте .nsi скрипт
3. Скомпилируйте инсталлятор

### Linux (AppImage/DEB/RPM)

Для Linux можно создать пакеты различных форматов или использовать AppImage для portable приложения.

## Автоматизация CI/CD

Пример для GitHub Actions:

```yaml
name: Build Executables
on: [push, pull_request]

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
    
    runs-on: ${{ matrix.os }}
    
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Build
      run: |
        cd test_suite_executor
        make setup
        make build
    
    - name: Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: test-suite-executor-${{ matrix.os }}
        path: test_suite_executor/dist/
```