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

echo [1/4] Обновление версии из pyproject.toml...
python "%~dp0update_version.py"
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Не удалось обновить версию
    exit /b 1
)

echo [2/4] Синхронизация зависимостей (включая dev)...
uv sync --dev
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Не удалось синхронизировать зависимости
    exit /b 1
)

echo [3/4] Создание исполняемого файла...
uv run pyinstaller build_scripts\test_suite_executor.spec --clean
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Не удалось создать исполняемый файл
    exit /b 1
)

echo [4/4] Проверка результата...
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