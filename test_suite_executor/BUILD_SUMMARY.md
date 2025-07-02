# Сборка исполняемых файлов - Резюме

## Что добавлено

В проект `test_suite_executor` добавлена возможность создания исполняемых файлов для:
- **Windows** (.exe)
- **Linux** (bin)

Сборка происходит из Windows с использованием PyInstaller и Docker.

## Новые файлы

| Файл | Назначение |
|------|-----------|
| `test_suite_executor.spec` | Конфигурация PyInstaller |
| `build_windows.bat` | Сборка Windows exe |
| `build_linux.bat` | Сборка Linux bin через Docker |
| `build_all.bat` | Сборка всех платформ |
| `Dockerfile.build` | Docker образ для Linux сборки |
| `BUILD_TROUBLESHOOTING.md` | Устранение неполадок |

## Обновленные файлы

| Файл | Изменения |
|------|-----------|
| `pyproject.toml` | Добавлен PyInstaller, создан console script |
| `README.md` | Добавлена документация по сборке |

## Быстрый старт

### Сборка Windows exe
```cmd
cd test_suite_executor
build_windows.bat
```

### Сборка Linux bin (требует Docker)
```cmd
cd test_suite_executor
build_linux.bat
```

### Сборка всех платформ
```cmd
cd test_suite_executor
build_all.bat
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

✅ **Задача выполнена**: Добавлена возможность создания exe и bin файлов из Windows