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


def test_add_select_app(eng):
    with Session(eng) as session:
        app1 = Application(
            app_id=uuid.uuid4(), app_name="test1", secret="secret"
        )
        session.add(app1)
        selected_app = session.scalar(
            sqlalchemy.select(Application).where(
                Application.app_name == "test1"
            )
        )
        session.commit()
        assert selected_app is not None
        assert selected_app.app_id == app1.app_id
