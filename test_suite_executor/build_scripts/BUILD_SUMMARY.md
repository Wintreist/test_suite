# Сборка исполняемых файлов - Резюме

## Что добавлено

В проект `test_suite_executor` добавлена возможность создания исполняемых файлов для:
- **Windows** (.exe) - собирается на Windows
- **Linux** (bin) - собирается на Linux  
- **macOS** (bin) - собирается на macOS (экспериментально)

Каждая платформа собирается нативно на соответствующей ОС.

## Новые файлы

### В директории `build_scripts/`:
| Файл | Назначение |
|------|-----------|
| `test_suite_executor.spec` | Конфигурация PyInstaller |
| `build_windows.bat` | Сборка Windows exe (только Windows) |
| `build_linux.sh` | Сборка Linux/macOS bin |
| `build.py` | Универсальный скрипт (автоопределение ОС) |
| `update_version.py` | Синхронизация версии из pyproject.toml |
| `BUILD_TROUBLESHOOTING.md` | Устранение неполадок |

### В корне проекта:
| Файл | Назначение |
|------|-----------|
| `build.bat` | Wrapper для Windows |
| `build.sh` | Wrapper для Linux/macOS |

## Обновленные файлы

| Файл | Изменения |
|------|-----------|
| `pyproject.toml` | Добавлен console script, PyInstaller в dev зависимости |
| `src/test_suite_executor/_version.py` | Создан модуль версионирования |
| `src/test_suite_executor/runner.py` | Использует _version вместо pyproject.toml |
| `README.md` | Добавлена документация по сборке |

## Быстрый старт

### Универсальная сборка (рекомендуется)
```bash
cd test_suite_executor

# Windows:
build.bat

# Linux/macOS:
./build.sh

# Или напрямую:
python build_scripts/build.py
```

### Сборка для конкретной платформы

**Windows:**
```cmd
cd test_suite_executor
build_scripts\build_windows.bat
```

**Linux/macOS:**
```bash
cd test_suite_executor
./build_scripts/build_linux.sh
```



## Результат

Исполняемые файлы создаются в папке `dist/`:
- `dist/test-suite-executor.exe` (Windows)
- `dist/test-suite-executor` (Linux)

## Использование

```bash
# Windows
.\dist\test-suite-executor.exe

# Linux
./dist/test-suite-executor
```

Исполняемые файлы **самодостаточны** и не требуют установки Python или зависимостей.

## Размер файлов

Ожидаемый размер исполняемых файлов: **50-100 MB** (включает Python runtime и все зависимости).

## Поддержка

- При проблемах сборки см. `BUILD_TROUBLESHOOTING.md`
- Все временные файлы автоматически исключены в `.gitignore`

---

✅ **Задача выполнена**: Добавлена возможность создания exe и bin файлов
- Windows exe собирается на Windows
- Linux bin собирается на Linux  
- Универсальный скрипт для автоматического определения ОС
- Больше не требуется Docker для кроссплатформенной сборки
- **ИСПРАВЛЕНО**: Проблема с `FileNotFoundError: pyproject.toml` в исполняемых файлах
- **ДОБАВЛЕНО**: Автоматическое встраивание версии и названия проекта в исполняемые файлы