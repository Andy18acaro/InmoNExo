import pytest
from sqlalchemy import inspect

from inmonexo_db.models import Base


def test_core_tables_exist(sqlite_engine) -> None:
    tables = set(inspect(sqlite_engine).get_table_names())
    expected = {
        "districts",
        "district_aliases",
        "companies",
        "projects",
        "units",
        "price_history",
        "events",
        "scrape_runs",
    }
    assert expected.issubset(tables)
