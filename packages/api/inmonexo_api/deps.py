from collections.abc import Generator

from sqlalchemy.orm import Session

from inmonexo_db.session import get_session_factory

_session_factory = get_session_factory()


def get_db() -> Generator[Session, None, None]:
    session = _session_factory()
    try:
        yield session
    finally:
        session.close()
