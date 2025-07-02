# Test Suite Executor

FastAPI приложение для асинхронного запуска pytest тестов с возможностью отслеживания статуса выполнения.

## Особенности

- **Асинхронный запуск**: Тесты запускаются в фоновом режиме
- **Контроль одновременности**: В каждый момент времени может выполняться только один тест
- **Отслеживание статуса**: Возможность получения информации о ходе выполнения тестов
- **История запусков**: Сохранение информации о всех запусках

## API Endpoints

### POST /run_suite
Запуск нового теста в фоновом режиме.

**Request Body:**
```json
{
  "repo_url": "ssh://git@src.axxonsoft.dev/qa/example_autotests.git",
  "branch": "main",
  "suite": {
    "name": "tests/",
    "params": {
      "alluredir": "/tmp/allure-reports"
    },
    "print_output": true
  }
}
```

**Response:**
```json
{
  "test_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "accepted",
  "message": "Тест принят к исполнению"
}
```

**Status Codes:**
- `200` - Тест принят к исполнению
- `409` - В данный момент уже запущен другой тест

### GET /test_status/{test_id}
Получение статуса выполнения конкретного теста.

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "created_at": "2024-01-15T10:30:00",
  "started_at": "2024-01-15T10:30:05",
  "completed_at": null,
  "result": null,
  "error": null
}
```

**Status Values:**
- `pending` - Тест принят, но еще не начал выполняться
- `running` - Тест выполняется
- `completed` - Тест успешно завершен
- `failed` - Тест завершился с ошибкой

### GET /current_test
Получение информации о текущем выполняющемся тесте.

**Response (если тест выполняется):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "created_at": "2024-01-15T10:30:00",
  "started_at": "2024-01-15T10:30:05"
}
```

**Response (если тесты не выполняются):**
```json
{
  "message": "В данный момент тесты не выполняются"
}
```

### GET /test_history
Получение истории всех запусков тестов.

**Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00",
    "started_at": "2024-01-15T10:30:05",
    "completed_at": "2024-01-15T10:45:00",
    "result": {
      "name": "tests/",
      "params": {...},
      "result_code": 0
    },
    "error": null
  }
]
```

### DELETE /test_history
Очистка истории тестов (кроме текущего выполняющегося).

**Response:**
```json
{
  "message": "История тестов очищена"
}
```

## Запуск приложения

```bash
cd test_suite_executor
uv sync
uv run python -m test_suite_executor.runner
```

Приложение будет доступно по адресу: `http://localhost:8888`

## Примеры использования

### Запуск теста
```bash
curl -X POST "http://localhost:8888/run_suite" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "ssh://git@example.com/repo.git",
    "branch": "main",
    "suite": {
      "name": "tests/",
      "params": {
        "alluredir": "/tmp/allure"
      }
    }
  }'
```

### Проверка статуса
```bash
curl "http://localhost:8888/test_status/550e8400-e29b-41d4-a716-446655440000"
```

### Получение текущего теста
```bash
curl "http://localhost:8888/current_test"
```

## Сборка исполняемых файлов

Проект поддерживает создание исполняемых файлов для Windows (exe) и Linux (bin) с использованием PyInstaller.

### Предварительные требования

**Для Windows:**
- [uv](https://github.com/astral-sh/uv) - менеджер пакетов Python
- Windows 10/11

**Для Linux (через Docker):**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) - для кроссплатформенной сборки

### Сборка для Windows

```cmd
# Из папки test_suite_executor
build_windows.bat
```

Результат: `dist\test-suite-executor.exe`

### Сборка для Linux

```cmd
# Из папки test_suite_executor (требует Docker)
build_linux.bat
```

Результат: `dist\test-suite-executor`

### Сборка для всех платформ

```cmd
# Сборка Windows и Linux версий одновременно
build_all.bat
```

### Использование исполняемых файлов

**Windows:**
```cmd
.\dist\test-suite-executor.exe
```

**Linux:**
```bash
./dist/test-suite-executor
```

Исполняемые файлы самодостаточны и не требуют установки Python или зависимостей.

## Настройка

Приложение можно настроить через переменные окружения:

- `ExecutorSettings__port` - порт для запуска (по умолчанию 8888)

Пример:
```bash
export ExecutorSettings__port=9000
uv run python -m test_suite_executor.runner
```