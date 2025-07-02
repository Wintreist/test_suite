def application():
    from pathlib import Path

    import tomllib
    from fastapi import FastAPI

    from test_suite_executor.server.run_suite import router

    pyproject = tomllib.loads(Path("pyproject.toml").read_text())
    project = pyproject["project"]

    app = FastAPI(
        title=project["name"],
        version=project["version"],
    )
    app.include_router(router)
    return app


def main():
    import uvicorn

    from test_suite_executor.settings import ExecutorSettings

    settings = ExecutorSettings()

    uvicorn.run(
        app=application(),
        # host="0.0.0.0",
        port=settings.port,
    )


if __name__ == "__main__":
    main()
