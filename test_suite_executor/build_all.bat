@echo off
echo ========================================
echo   Сборка test-suite-executor для Windows
echo ========================================

echo [INFO] Сборка для Linux выполняется на Linux системе!
echo        Для Linux используйте: ./build_linux.sh
echo.

echo [ЭТАП 1] Сборка для Windows...
call build_windows.bat
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Ошибка при сборке Windows версии
    echo ========================================
    echo Проверьте сообщения об ошибках выше
) else (
    echo ✅ Windows версия собрана успешно!
    echo ========================================
    echo.
    echo Созданный файл:
    if exist "dist\test-suite-executor.exe" (
        echo   Windows: dist\test-suite-executor.exe
    )
    echo.
    echo Для запуска:
    echo   Windows: .\dist\test-suite-executor.exe
    echo.
    echo Для сборки Linux версии:
    echo   1. Скопируйте проект на Linux систему
    echo   2. Запустите: ./build_linux.sh
)

echo.
pause