"""ASGI entrypoint: uvicorn apps.api.main:app"""

from inmonexo_api.app import create_app

app = create_app()
