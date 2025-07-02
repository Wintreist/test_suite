# -*- mode: python ; coding: utf-8 -*-
import sys
import os
from pathlib import Path

# Получаем путь к родительской директории (test_suite_executor)
project_root = Path(__file__).parent.parent

# Добавляем путь к модулю test_suite
sys.path.insert(0, str(project_root.parent / 'test_suite' / 'src'))

a = Analysis(
    [str(project_root / 'src' / 'test_suite_executor' / 'runner.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        # pyproject.toml больше не нужен, используем _version.py
    ],
    hiddenimports=[
        'test_suite_executor',
        'test_suite_executor.runner',
        'test_suite_executor.server',
        'test_suite_executor.server.run_suite',
        'test_suite_executor.models',
        'test_suite_executor.models.suite',
        'test_suite_executor.settings',
        'test_suite_executor._version',
        'test_suite.pytest',
        'test_suite.base',
        'uvicorn',
        'fastapi',
        'pydantic',
        'pydantic_settings',
        'git',
        'object_storage',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='test-suite-executor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)