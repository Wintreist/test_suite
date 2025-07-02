@echo off
echo ========================================
echo   Сборка test-suite-executor для Linux
echo ========================================

REM Проверяем наличие Docker
docker --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Docker не установлен или не запущен.
    echo Установите Docker Desktop и убедитесь что он запущен.
    exit /b 1
)

echo [1/4] Создание директории для результата...
if not exist "dist" mkdir dist

echo [2/4] Сборка Docker образа...
docker build -f Dockerfile.build -t test-suite-executor-builder .
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Не удалось собрать Docker образ
    exit /b 1
)

echo [3/4] Запуск контейнера и извлечение бинарника...
docker run --rm -v "%cd%\dist:/output" test-suite-executor-builder cp /app/test_suite_executor/dist/test-suite-executor /output/
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Не удалось скопировать бинарник
    exit /b 1
)

echo [4/4] Проверка результата...
if exist "dist\test-suite-executor" (
    echo ✅ Успешно создан: dist\test-suite-executor
    dir dist\test-suite-executor
) else (
    echo ❌ Файл не был создан
    exit /b 1
)

echo.
echo ========================================
echo   Сборка завершена успешно!
echo ========================================
echo Linux бинарник: dist\test-suite-executor
echo.
pause