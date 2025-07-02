.PHONY: build-linux build-windows clean install-deps help setup test

# Переменные
PYTHON := python3
VENV_DIR := .venv
DIST_DIR := dist
BUILD_DIR := build

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Настройка окружения разработки
	@echo "Настройка окружения разработки..."
	$(PYTHON) -m venv $(VENV_DIR)
ifeq ($(OS),Windows_NT)
	$(VENV_DIR)\Scripts\activate && pip install -e .[build]
else
	. $(VENV_DIR)/bin/activate && pip install -e .[build]
endif
	@echo "Окружение настроено!"

install-deps: ## Установить зависимости для сборки
	@echo "Установка зависимостей для сборки..."
ifeq ($(OS),Windows_NT)
	pip install -e .[build]
else
	pip install -e .[build]
endif

clean: ## Очистить файлы сборки
	@echo "Очистка файлов сборки..."
	rm -rf $(DIST_DIR)
	rm -rf $(BUILD_DIR)
	rm -rf *.spec
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true

build-linux: ## Собрать исполняемый файл для Linux
	@echo "Сборка для Linux..."
	./build_scripts/build_linux.sh

build-windows: ## Собрать исполняемый файл для Windows
	@echo "Сборка для Windows..."
	build_scripts\build_windows.bat

test: ## Запустить тесты
	@echo "Запуск тестов..."
ifeq ($(OS),Windows_NT)
	$(VENV_DIR)\Scripts\python -m pytest tests/
else
	$(VENV_DIR)/bin/python -m pytest tests/
endif

run-dev: ## Запустить сервер в режиме разработки
	@echo "Запуск сервера в режиме разработки..."
ifeq ($(OS),Windows_NT)
	$(VENV_DIR)\Scripts\python main.py
else
	$(VENV_DIR)/bin/python main.py
endif

# Автоматическое определение платформы и сборка
build: ## Собрать исполняемый файл для текущей платформы
ifeq ($(OS),Windows_NT)
	$(MAKE) build-windows
else
	$(MAKE) build-linux
endif

all: clean setup build ## Полная пересборка

test-executable: ## Тестировать собранный исполняемый файл
	@echo "Тестирование исполняемого файла..."
	pip install requests
	python test_executable.py

package: build ## Создать архив с исполняемым файлом
	@echo "Создание архива..."
ifeq ($(OS),Windows_NT)
	cd $(DIST_DIR) && tar -czf test-suite-executor-windows.tar.gz test-suite-executor.exe
	@echo "Архив создан: $(DIST_DIR)/test-suite-executor-windows.tar.gz"
else
	cd $(DIST_DIR) && tar -czf test-suite-executor-linux.tar.gz test-suite-executor
	@echo "Архив создан: $(DIST_DIR)/test-suite-executor-linux.tar.gz"
endif

build-and-test: build test-executable ## Сборка и тестирование исполняемого файла