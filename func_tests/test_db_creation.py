import uuid

import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from src.homework.db.engine import engine
from src.homework.db.models import Base, Application


@pytest.fixture(name="eng")
def db_creation():
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


def test_database_works_correctly(eng):
    with Session(eng) as session:
        app_id = uuid.uuid4()
        app1 = Application(app_id=app_id, app_name="test1", secret="secret")
        session.add(app1)
        session.commit()
    with Session(eng) as session:
        selected_app = session.scalar(
            sqlalchemy.select(Application).where(
                Application.app_name == "test1"
            )
        )
        assert selected_app is not None
        assert selected_app.app_id == app_id
