@echo off
echo ========================================
echo   Сборка test-suite-executor для всех платформ
echo ========================================

set BUILD_SUCCESS=1

echo [ЭТАП 1] Сборка для Windows...
call build_windows.bat
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Ошибка при сборке Windows версии
    set BUILD_SUCCESS=0
) else (
    echo ✅ Windows версия собрана успешно
)

echo.
echo [ЭТАП 2] Сборка для Linux...
call build_linux.bat
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Ошибка при сборке Linux версии
    set BUILD_SUCCESS=0
) else (
    echo ✅ Linux версия собрана успешно
)

echo.
echo ========================================
if %BUILD_SUCCESS%==1 (
    echo   ✅ ВСЕ ПЛАТФОРМЫ СОБРАНЫ УСПЕШНО!
    echo ========================================
    echo.
    echo Созданные файлы:
    if exist "dist\test-suite-executor.exe" (
        echo   Windows: dist\test-suite-executor.exe
    )
    if exist "dist\test-suite-executor" (
        echo   Linux:   dist\test-suite-executor
    )
    echo.
    echo Для запуска:
    echo   Windows: .\dist\test-suite-executor.exe
    echo   Linux:   ./dist/test-suite-executor
) else (
    echo   ❌ ОШИБКИ ПРИ СБОРКЕ
    echo ========================================
    echo Проверьте сообщения об ошибках выше
)

echo.
pause