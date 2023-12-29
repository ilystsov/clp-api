import uuid

import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from src.homework.app import create_app
from src.homework.api.security import (
    issue_token,
    MasterAccessLevel,
)
from src.homework.api.contracts import AccessLevel
from src.homework.db.models import Application
from src.homework.db.engine import engine
from src.homework.db.models import Base


@pytest.fixture(name="eng")
def create_db():
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(name="client")
def create_client(eng):
    app = create_app()
    client = TestClient(app)
    return client


@pytest.fixture(name="inserted_app")
def insert_app(eng):
    with Session(eng) as session:
        app_id, secret = uuid.uuid4(), "secret"
        new_app = Application(
            app_id=app_id, app_name=str(app_id)[:30], secret=secret
        )
        session.add(new_app)
        session.commit()
    yield str(app_id), secret


@pytest.fixture(name="master_app")
def create_master_app(inserted_app):
    yield issue_token(
        app_id=inserted_app[0],
        secret=inserted_app[1],
        access_level=MasterAccessLevel("MasterApp"),
    )


@pytest.fixture(name="read_app")
def create_read_app(inserted_app):
    yield inserted_app[0], issue_token(
        app_id=inserted_app[0],
        secret=inserted_app[1],
        access_level=AccessLevel("Can_Read"),
    )


@pytest.fixture(name="modify_app")
def create_modify_app(inserted_app):
    yield inserted_app[0], issue_token(
        app_id=inserted_app[0],
        secret=inserted_app[1],
        access_level=AccessLevel("Can_Modify_Orders"),
    )
