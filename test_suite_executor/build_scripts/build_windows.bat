@echo off
echo ========================================
echo   Сборка test-suite-executor для Windows
echo ========================================

REM Проверяем наличие uv
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: uv не установлен. Установите uv сначала.
    exit /b 1
)

cd /d "%~dp0.."

echo [1/3] Синхронизация зависимостей (включая dev)...
uv sync --dev
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Не удалось синхронизировать зависимости
    exit /b 1
)

echo [2/3] Создание исполняемого файла...
uv run pyinstaller build_scripts\test_suite_executor.spec --clean
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Не удалось создать исполняемый файл
    exit /b 1
)

echo [3/3] Проверка результата...
if exist "dist\test-suite-executor.exe" (
    echo ✅ Успешно создан: dist\test-suite-executor.exe
    dir dist\test-suite-executor.exe
) else (
    echo ❌ Файл не был создан
    exit /b 1
)

echo.
echo ========================================
echo   Сборка завершена успешно!
echo ========================================
echo Исполняемый файл: dist\test-suite-executor.exe
echo.
pause