#!/bin/bash
echo "Запуск сборки test-suite-executor..."
cd "$(dirname "$0")"
python3 build_scripts/build.py