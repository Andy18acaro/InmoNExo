from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from inmonexo_db.config import Settings
from inmonexo_db.models import Base


def get_engine(settings: Settings | None = None):
    settings = settings or Settings()
    return create_engine(settings.sqlalchemy_url, future=True)


def init_db(settings: Settings | None = None) -> None:
    engine = get_engine(settings)
    Base.metadata.create_all(engine)


def get_session_factory(settings: Settings | None = None):
    engine = get_engine(settings)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
