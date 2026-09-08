import pytest

from inmonexo_db.models import Base
from inmonexo_db.session import get_engine, get_session_factory, init_db


@pytest.fixture
def sqlite_engine(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    init_db()
    yield get_engine()
    Base.metadata.drop_all(get_engine())


@pytest.fixture
def db_session(sqlite_engine):
    factory = get_session_factory()
    session = factory()
    try:
        yield session
    finally:
        session.close()
