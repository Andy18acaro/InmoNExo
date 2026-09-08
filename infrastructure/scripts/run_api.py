#!/usr/bin/env python3
"""Run the InmoNExo read API locally."""

import os

import uvicorn


def main() -> None:
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8100"))
    uvicorn.run("inmonexo_api.app:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    main()
