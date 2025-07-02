def application():
    from fastapi import FastAPI

    from test_suite_executor.server.run_suite import router
    from test_suite_executor._version import __title__, __version__

    app = FastAPI(
        title=__title__,
        version=__version__,
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
