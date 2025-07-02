#!/usr/bin/env python3
"""
Универсальный скрипт сборки test-suite-executor
Автоматически определяет ОС и запускает соответствующий скрипт сборки
"""

import os
import sys
import subprocess
import platform


def main():
    print("=" * 50)
    print("  Универсальная сборка test-suite-executor")
    print("=" * 50)
    
    # Определяем операционную систему
    system = platform.system().lower()
    print(f"Обнаружена ОС: {platform.system()} ({platform.machine()})")
    print()
    
    if system == "windows":
        print("🪟 Запуск сборки для Windows...")
        script = "build_windows.bat"
        try:
            result = subprocess.run([script], shell=True, check=True)
            print("✅ Сборка Windows завершена успешно!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка при сборке Windows: {e}")
            sys.exit(1)
            
    elif system == "linux":
        print("🐧 Запуск сборки для Linux...")
        script = "./build_linux.sh"
        
        # Проверяем что скрипт исполняемый
        if not os.access("build_linux.sh", os.X_OK):
            print("Делаем скрипт исполняемым...")
            os.chmod("build_linux.sh", 0o755)
            
        try:
            result = subprocess.run([script], check=True)
            print("✅ Сборка Linux завершена успешно!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка при сборке Linux: {e}")
            sys.exit(1)
            
    elif system == "darwin":
        print("🍎 macOS обнаружена")
        print("Попробуем использовать Linux скрипт...")
        script = "./build_linux.sh"
        
        # Проверяем что скрипт исполняемый
        if not os.access("build_linux.sh", os.X_OK):
            print("Делаем скрипт исполняемым...")
            os.chmod("build_linux.sh", 0o755)
            
        try:
            result = subprocess.run([script], check=True)
            print("✅ Сборка macOS завершена успешно!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка при сборке macOS: {e}")
            sys.exit(1)
            
    else:
        print(f"❌ Неподдерживаемая ОС: {system}")
        print("Поддерживаются: Windows, Linux, macOS")
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("🎉 Сборка завершена!")
    print("=" * 50)
    
    # Показываем результат
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        print("Созданные файлы:")
        for file in os.listdir(dist_dir):
            file_path = os.path.join(dist_dir, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                print(f"  📦 {file} ({size // (1024*1024)} MB)")
    
    print()
    if system == "windows":
        print("Запуск: .\\dist\\test-suite-executor.exe")
    else:
        print("Запуск: ./dist/test-suite-executor")


if __name__ == "__main__":
    main()