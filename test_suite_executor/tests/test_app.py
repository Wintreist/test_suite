#!/usr/bin/env python3
"""
Простой тест для проверки работы API
"""

import json
import time
import requests

BASE_URL = "http://localhost:8888"

def test_current_test():
    """Тестируем получение информации о текущем тесте (должно быть пусто)"""
    response = requests.get(f"{BASE_URL}/current_test")
    print(f"GET /current_test: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_run_suite():
    """Тестируем запуск теста (с мок-данными)"""
    # Создаем мок-данные для запроса
    request_data = {
        "repo_url": "https://github.com/example/mock-repo.git",
        "branch": "main",
        "suite": {
            "name": "tests/",
            "params": {
                "alluredir": "/tmp/allure-reports"
            },
            "print_output": True
        }
    }
    
    print("Отправляем запрос на запуск теста...")
    response = requests.post(f"{BASE_URL}/run_suite", json=request_data)
    print(f"POST /run_suite: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {result}")
        test_id = result.get("test_id")
        
        if test_id:
            # Проверяем статус теста
            print(f"\nПроверяем статус теста {test_id}...")
            status_response = requests.get(f"{BASE_URL}/test_status/{test_id}")
            print(f"GET /test_status/{test_id}: {status_response.status_code}")
            print(f"Status response: {status_response.json()}")
            
            # Проверяем текущий тест
            print(f"\nПроверяем текущий выполняющийся тест...")
            current_response = requests.get(f"{BASE_URL}/current_test")
            print(f"GET /current_test: {current_response.status_code}")
            print(f"Current test: {current_response.json()}")
            
    else:
        print(f"Error: {response.text}")
    print()

def test_history():
    """Тестируем получение истории"""
    response = requests.get(f"{BASE_URL}/test_history")
    print(f"GET /test_history: {response.status_code}")
    print(f"History: {response.json()}")
    print()

if __name__ == "__main__":
    print("Тестирование API Test Suite Executor")
    print("=" * 50)
    
    try:
        # Тест 1: Проверяем текущий тест (должен быть пустой)
        test_current_test()
        
        # Тест 2: Отправляем мок-запрос (ожидаем ошибку, так как репозиторий фейковый)
        test_run_suite()
        
        # Тест 3: Проверяем историю
        test_history()
        
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к API. Убедитесь, что сервер запущен на порту 8888")
    except Exception as e:
        print(f"❌ Ошибка: {e}")