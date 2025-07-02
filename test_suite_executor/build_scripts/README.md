# Скрипты сборки test-suite-executor

Эта директория содержит все файлы, необходимые для сборки исполняемых файлов проекта.

## Структура файлов

### Основные скрипты
- `build.py` - Универсальный скрипт сборки (автоопределение ОС)
- `build_windows.bat` - Сборка для Windows (.exe)
- `build_linux.sh` - Сборка для Linux/macOS (bin)
- `update_version.py` - Синхронизация версии из pyproject.toml

### Конфигурация
- `test_suite_executor.spec` - Конфигурация PyInstaller

### Документация
- `BUILD_SUMMARY.md` - Краткое описание добавленной функциональности
- `BUILD_TROUBLESHOOTING.md` - Устранение неполадок при сборке

## Использование

### Из корня проекта (рекомендуется):
```bash
# Windows
build.bat

# Linux/macOS  
./build.sh
```

### Напрямую из build_scripts/:
```bash
# Универсальный способ
python build.py

# Windows
build_windows.bat

# Linux/macOS
./build_linux.sh
```

## Результат

Исполняемые файлы создаются в `../dist/`:
- Windows: `test-suite-executor.exe`
- Linux/macOS: `test-suite-executor`

## Требования

- [uv](https://github.com/astral-sh/uv) - менеджер пакетов Python
- Python 3.12+
- Соответствующая ОС для целевой платформы

**Примечания:** 
- PyInstaller находится в dev зависимостях и устанавливается автоматически при выполнении `uv sync --dev`.
- Версия и метаданные автоматически синхронизируются из `pyproject.toml` в `_version.py` перед сборкой.

## Версионирование

Исполняемые файлы содержат встроенную информацию о версии и названии проекта. Вместо чтения `pyproject.toml` в runtime (что невозможно в собранном exe), используется модуль `_version.py`.

### Автоматическая синхронизация
Скрипты сборки автоматически обновляют `src/test_suite_executor/_version.py` из `pyproject.toml` перед сборкой.

### Ручная синхронизация
```bash
python build_scripts/update_version.py
```

## Структура проекта после сборки

```
test_suite_executor/
├── build_scripts/                    # Скрипты сборки
│   ├── build.py                     # Универсальный скрипт
│   ├── build_windows.bat            # Windows сборка
│   ├── build_linux.sh               # Linux сборка  
│   ├── test_suite_executor.spec     # Конфигурация PyInstaller
│   ├── README.md                    # Документация
│   ├── BUILD_SUMMARY.md             # Описание функциональности
│   └── BUILD_TROUBLESHOOTING.md     # Решение проблем
├── build.bat                        # Wrapper для Windows
├── build.sh                         # Wrapper для Linux
├── dist/                            # Результат сборки
│   ├── test-suite-executor.exe      # Windows исполняемый файл
│   └── test-suite-executor          # Linux исполняемый файл
└── ...
```