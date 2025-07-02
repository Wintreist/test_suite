#!/usr/bin/env python3
"""
Точка входа для test-suite-executor.
Этот файл используется PyInstaller для создания исполняемого файла.
"""

import sys
import os
from pathlib import Path

# Добавляем src директорию в Python path
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from test_suite_executor.runner import main

if __name__ == "__main__":
    main()