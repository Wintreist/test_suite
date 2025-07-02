"""
Заглушка для robo_settings
"""
from pathlib import Path


class ROBOSettings:
    """Заглушка для ROBOSettings"""
    
    def __init__(self):
        # Используем временную директорию по умолчанию
        self.ROBO_DIR = Path("/tmp/robo")
        self.ROBO_DIR.mkdir(exist_ok=True)