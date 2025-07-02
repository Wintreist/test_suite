import argparse
from pathlib import Path

from test_suite.pytest import PyTestSuite

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run PyTestSuite with params from json file")
    parser.add_argument("--params", required=True, help="Path to input params json file")
    parser.add_argument("--result", required=True, help="Path to output result json file")
    args = parser.parse_args()

    params_path = Path(args.params)
    result_path = Path(args.result)

    # Читаем параметры
    with params_path.open("r", encoding="utf-8") as f:
        data = f.read()

    # Создаём объект параметров через pydantic

    suite = PyTestSuite.model_validate_json(data)
    suite.run()

    # Сохраняем результат (весь объект PyTestSuite) в json
    with result_path.open("w", encoding="utf-8") as f:
        f.write(suite.model_dump_json())
