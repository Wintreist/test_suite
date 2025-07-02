"""
Информация о версии и метаданных проекта.
Этот файл содержит константы, которые используются вместо чтения pyproject.toml
в runtime для корректной работы в собранных исполняемых файлах.

ВНИМАНИЕ: Этот файл автоматически обновляется из pyproject.toml
Запустите: python build_scripts/update_version.py
"""

__version__ = "0.1.0"
__title__ = "test-suite-executor" 
__description__ = "Add your description here"
__author__ = "vikentiy.smetanin"
__author_email__ = "vikentiy.smetanin@axxonsoft.dev"

# Для совместимости
VERSION = __version__
TITLE = __title__
DESCRIPTION = __description__
