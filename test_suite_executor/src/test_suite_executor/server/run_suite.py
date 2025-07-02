import os
import shutil
import subprocess
import tempfile
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from threading import Lock
from typing import Dict, Optional

import git
from fastapi import APIRouter, BackgroundTasks, HTTPException
from test_suite.pytest.suite import PyTestSuite
from pydantic import BaseModel

from test_suite_executor.models.suite import SuiteRequest

router = APIRouter()
lock = Lock()

TEST_SUITE_RUN_TIMEOUT = 60 * 60


class TestStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class TestRunInfo(BaseModel):
    id: str
    status: TestStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[PyTestSuite] = None
    error: Optional[str] = None


# Глобальное хранилище состояний тестов
test_runs: Dict[str, TestRunInfo] = {}
current_running_test: Optional[str] = None


def run_test_suite_background(test_id: str, request: SuiteRequest):
    """Функция для запуска теста в фоновом режиме"""
    global current_running_test
    
    test_run = test_runs[test_id]
    
    try:
        test_run.status = TestStatus.RUNNING
        test_run.started_at = datetime.now()
        current_running_test = test_id
        
        work_dir = Path(tempfile.mkdtemp(prefix="test_suite_"))
        
        try:
            # Клонируем репозиторий и переключаемся на нужную ветку
            repo = git.Repo.clone_from(url=request.repo_url, to_path=work_dir, branch=request.branch)
            repo_dir = Path(repo.working_dir)
            
            # Создаём виртуальное окружение (venv)
            subprocess.run(["uv", "sync"], cwd=repo_dir, check=True)
            venv_dir = repo_dir.joinpath(".venv")
            assert venv_dir.exists()
            python_bin = (
                venv_dir.joinpath("Scripts", "python.exe") if os.name == "nt" else venv_dir.joinpath("bin", "python")
            )
            assert python_bin.exists()

            # Сохраняем параметры в json
            params_path = repo_dir.joinpath("suite_params.json")
            params_path.write_text(request.suite.model_dump_json(by_alias=True))
            result_path = repo_dir.joinpath("suite_result.json")

            # Запускаем run_suite.py
            if os.name == "nt":
                libs_path = venv_dir.joinpath("Lib", "site-packages")
            else:
                libs_path = venv_dir.joinpath("lib").glob("python*/site-packages").__next__()

            lib_test_suite_path = libs_path.joinpath("test_suite")
            test_suite_run_script = lib_test_suite_path.joinpath("pytest", "run_suite.py")
            
            subprocess.run(
                [str(python_bin), str(test_suite_run_script), "--params", str(params_path), "--result", str(result_path)],
                cwd=repo_dir,
                timeout=TEST_SUITE_RUN_TIMEOUT,
                check=True
            )

            # Читаем результат
            if not result_path.exists():
                raise Exception("Result file not found")
            result_json = PyTestSuite.model_validate_json(result_path.read_text())
            
            # Успешное завершение
            test_run.status = TestStatus.COMPLETED
            test_run.completed_at = datetime.now()
            test_run.result = result_json
            
        finally:
            # Чистим временную папку
            if work_dir.exists():
                shutil.rmtree(work_dir, ignore_errors=True)
                
    except subprocess.CalledProcessError as e:
        test_run.status = TestStatus.FAILED
        test_run.completed_at = datetime.now()
        test_run.error = f"Subprocess error: {e}"
    except subprocess.TimeoutExpired:
        test_run.status = TestStatus.FAILED
        test_run.completed_at = datetime.now()
        test_run.error = "Test execution timed out"
    except Exception as e:
        test_run.status = TestStatus.FAILED
        test_run.completed_at = datetime.now()
        test_run.error = str(e)
    finally:
        current_running_test = None


@router.post("/run_suite")
def run_suite_endpoint(request: SuiteRequest, background_tasks: BackgroundTasks):
    """Запуск теста в фоновом режиме"""
    global current_running_test
    
    # Проверяем, что нет запущенных тестов
    if current_running_test is not None:
        running_test = test_runs.get(current_running_test)
        if running_test and running_test.status == TestStatus.RUNNING:
            raise HTTPException(
                status_code=409, 
                detail=f"В данный момент уже запущен тест с ID: {current_running_test}"
            )
    
    # Создаем новый тест
    test_id = str(uuid.uuid4())
    test_run = TestRunInfo(
        id=test_id,
        status=TestStatus.PENDING,
        created_at=datetime.now()
    )
    
    test_runs[test_id] = test_run
    
    # Запускаем тест в фоне
    background_tasks.add_task(run_test_suite_background, test_id, request)
    
    return {
        "test_id": test_id,
        "status": "accepted",
        "message": "Тест принят к исполнению"
    }


@router.get("/test_status/{test_id}")
def get_test_status(test_id: str):
    """Получение статуса выполнения теста"""
    if test_id not in test_runs:
        raise HTTPException(status_code=404, detail="Тест с указанным ID не найден")
    
    return test_runs[test_id]


@router.get("/current_test")
def get_current_test():
    """Получение информации о текущем выполняющемся тесте"""
    if current_running_test is None:
        return {"message": "В данный момент тесты не выполняются"}
    
    return test_runs[current_running_test]


@router.get("/test_history")
def get_test_history():
    """Получение истории всех запусков тестов"""
    return list(test_runs.values())


@router.delete("/test_history")
def clear_test_history():
    """Очистка истории тестов (кроме текущего выполняющегося)"""
    global test_runs
    
    if current_running_test is not None:
        # Сохраняем только текущий выполняющийся тест
        test_runs = {current_running_test: test_runs[current_running_test]}
    else:
        test_runs.clear()
    
    return {"message": "История тестов очищена"}
