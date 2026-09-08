import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from inmonexo_api.routers import analytics, companies, events, projects

STATIC_DIR = Path(__file__).parent / "static"

DEFAULT_CORS_ORIGINS = [
    "http://127.0.0.1:3100",
    "http://localhost:3100",
]


class StripSvcPrefixMiddleware(BaseHTTPMiddleware):
    """Strip /svc from public Vercel rewrites; internal bindings keep bare paths."""

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.scope["path"]
        if path == "/svc" or path.startswith("/svc/"):
            request.scope["path"] = path[4:] or "/"
        return await call_next(request)


def cors_origins() -> list[str]:
    extra = os.getenv("CORS_ORIGINS", "")
    origins = list(DEFAULT_CORS_ORIGINS)
    if extra:
        origins.extend(origin.strip() for origin in extra.split(",") if origin.strip())
    return origins


def create_app() -> FastAPI:
    root_path = os.getenv("FASTAPI_ROOT_PATH", "/svc" if os.getenv("VERCEL") else "")
    app = FastAPI(
        title="InmoNExo API",
        description="Read API for Lima real estate market intelligence",
        version="0.1.0",
        root_path=root_path,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins(),
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

    if os.getenv("VERCEL"):
        app.add_middleware(StripSvcPrefixMiddleware)

    return app


app = create_app()
