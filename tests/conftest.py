import pytest

from crm_core.db.base import get_db_session


@pytest.fixture()
def db_session():
    session = get_db_session()
    try:
        yield session
    finally:
        try:
            session.rollback()
        finally:
            session.close()
