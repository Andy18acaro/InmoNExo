from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from inmonexo_api.routers import analytics, companies, events, projects

STATIC_DIR = Path(__file__).parent / "static"

CORS_ORIGINS = [
    "http://127.0.0.1:3100",
    "http://localhost:3100",
]


def create_app() -> FastAPI:
    app = FastAPI(
        title="InmoNExo API",
        description="Read API for Lima real estate market intelligence",
        version="0.1.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app.include_router(companies.router)
    app.include_router(projects.router)
    app.include_router(events.router)
    app.include_router(analytics.router)

    @app.get("/", include_in_schema=False)
    def dashboard() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    if STATIC_DIR.is_dir():
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    return app


app = create_app()
