@echo off
chcp 65001 >nul
echo Запуск сборки test-suite-executor...
cd /d "%~dp0"
python build_scripts\build.py
pause