#!/usr/bin/env python3
"""
Скрипт для тестирования собранного исполняемого файла test-suite-executor.
"""

import subprocess
import sys
import time
import requests
import os
from pathlib import Path


def test_executable():
    """Тестирует работу исполняемого файла."""
    
    # Определяем путь к исполняемому файлу
    if os.name == 'nt':
        executable_path = Path("dist/test-suite-executor.exe")
    else:
        executable_path = Path("dist/test-suite-executor")
    
    if not executable_path.exists():
        print(f"❌ Исполняемый файл не найден: {executable_path}")
        return False
    
    print(f"✅ Исполняемый файл найден: {executable_path}")
    
    # Запускаем исполняемый файл
    print("🚀 Запуск исполняемого файла...")
    
    env = os.environ.copy()
    env["ExecutorSettings__port"] = "18888"  # Используем другой порт для тестирования
    
    try:
        process = subprocess.Popen(
            [str(executable_path)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Ждем запуска сервера
        print("⏳ Ожидание запуска сервера...")
        time.sleep(10)
        
        # Проверяем, что процесс еще запущен
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"❌ Процесс завершился неожиданно")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False
        
        # Проверяем доступность API
        print("🔍 Проверка доступности API...")
        try:
            response = requests.get("http://localhost:18888/docs", timeout=5)
            if response.status_code == 200:
                print("✅ API доступен, документация Swagger загружается")
            else:
                print(f"⚠️  API отвечает, но с кодом: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ API недоступен: {e}")
            return False
        
        # Проверяем endpoint health (если есть)
        try:
            response = requests.get("http://localhost:18888/", timeout=5)
            print(f"✅ Root endpoint отвечает с кодом: {response.status_code}")
        except requests.exceptions.RequestException:
            print("ℹ️  Root endpoint недоступен (это нормально)")
        
        print("✅ Тестирование завершено успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False
    
    finally:
        # Завершаем процесс
        if 'process' in locals():
            try:
                process.terminate()
                process.wait(timeout=5)
                print("🛑 Сервер остановлен")
            except subprocess.TimeoutExpired:
                process.kill()
                print("🛑 Сервер принудительно остановлен")


def main():
    """Главная функция."""
    print("🧪 Тестирование исполняемого файла test-suite-executor")
    print("=" * 60)
    
    if test_executable():
        print("\n🎉 Все тесты прошли успешно!")
        sys.exit(0)
    else:
        print("\n💥 Тестирование провалено!")
        sys.exit(1)


if __name__ == "__main__":
    main()