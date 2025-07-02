#!/usr/bin/env python3
"""
Скрипт для синхронизации версии и метаданных из pyproject.toml в _version.py
Это обеспечивает актуальность информации в собранных исполняемых файлах.
"""

import os
import sys
import tomllib
from pathlib import Path


def update_version():
    # Путь к корню проекта
    project_root = Path(__file__).parent.parent
    
    # Читаем pyproject.toml
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        print(f"❌ Файл {pyproject_path} не найден")
        sys.exit(1)
    
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)
    
    project = pyproject["project"]
    
    # Извлекаем данные
    version = project["version"]
    name = project["name"]
    description = project.get("description", "")
    
    author_info = project.get("authors", [{}])[0] if project.get("authors") else {}
    author = author_info.get("name", "")
    author_email = author_info.get("email", "")
    
    # Путь к _version.py
    version_path = project_root / "src" / "test_suite_executor" / "_version.py"
    
    # Создаем содержимое файла
    content = f'''"""
Информация о версии и метаданных проекта.
Этот файл содержит константы, которые используются вместо чтения pyproject.toml
в runtime для корректной работы в собранных исполняемых файлах.

ВНИМАНИЕ: Этот файл автоматически обновляется из pyproject.toml
Запустите: python build_scripts/update_version.py
"""

__version__ = "{version}"
__title__ = "{name}" 
__description__ = "{description}"
__author__ = "{author}"
__author_email__ = "{author_email}"

# Для совместимости
VERSION = __version__
TITLE = __title__
DESCRIPTION = __description__
'''
    
    # Записываем файл
    with open(version_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Обновлен {version_path}")
    print(f"   Версия: {version}")
    print(f"   Название: {name}")
    print(f"   Описание: {description}")


if __name__ == "__main__":
    update_version()