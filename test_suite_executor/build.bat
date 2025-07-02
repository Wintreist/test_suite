@echo off
echo Запуск сборки test-suite-executor...
cd /d "%~dp0"
python build_scripts\build.py
pause