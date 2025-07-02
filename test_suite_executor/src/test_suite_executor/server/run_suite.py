import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from threading import Lock

import git
from fastapi import APIRouter, HTTPException
from test_suite.pytest.suite import PyTestSuite

from test_suite_executor.models.suite import SuiteRequest

router = APIRouter()
lock = Lock()

TEST_SUITE_RUN_TIMEOUT = 60 * 60


@router.post("/run_suite")
def run_suite_endpoint(request: SuiteRequest):
    if lock.locked():
        raise HTTPException(status_code=409, detail="В данный момент уже запущен тест")
    with lock:
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

            # 7. Запускаем run_suite.py
            if os.name == "nt":
                libs_path = venv_dir.joinpath("Lib", "site-packages")

            lib_test_suite_path = libs_path.joinpath("test_suite")
            test_suite_run_script = lib_test_suite_path.joinpath("pytest", "run_suite.py")
            subprocess.run(
                [str(python_bin), str(test_suite_run_script), "--params", str(params_path), "--result", str(result_path)],
                cwd=repo_dir,
                timeout=TEST_SUITE_RUN_TIMEOUT,
            )

            # 8. Читаем результат
            if not result_path.exists():
                raise HTTPException(status_code=500, detail="Result file not found")
            result_json = PyTestSuite.model_validate_json(result_path.read_text())
            return result_json
        except subprocess.CalledProcessError as e:
            raise HTTPException(status_code=500, detail=f"Subprocess error: {e}")
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=500, detail="Test execution timed out")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            # Чистим временную папку
            if work_dir.exists():
                shutil.rmtree(work_dir, ignore_errors=True)
