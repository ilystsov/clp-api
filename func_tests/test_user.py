import pytest
from sqlalchemy.orm import Session
from src.homework.db.models import User
from func_tests.general_fixtures import (  # noqa: F401
    create_client,
    create_master_app,
    create_read_app,
    create_modify_app,
    create_db,
    insert_app,
)


@pytest.fixture(name="inserted_user")
def insert_user(eng):
    with Session(eng) as session:
        new_user = User(
            user_id=1, current_balance=1000, num_of_deleted_orders=1
        )
        session.add(new_user)
        session.commit()
        return new_user.user_id


@pytest.mark.parametrize("created_app", ["master_app", "modify_app"])
def test_get_balance_invalid_token(client, created_app, request):
    created_app = request.getfixturevalue(created_app)
    response = client.get(
        "/user/",
        headers={"token": created_app[1]},
        params={"user_id": 12345},
    )
    assert response.status_code == 403


def test_get_balance_not_found(client, read_app):
    non_existent_user_id = 100
    response = client.get(
        "/user/",
        headers={"token": read_app[1]},
        params={"user_id": non_existent_user_id},
    )
    assert response.status_code == 404


def test_get_balance(client, read_app, inserted_user):
    response = client.get(
        "/user/",
        headers={"token": read_app[1]},
        params={"user_id": inserted_user},
    )
    assert response.status_code == 200
    jsonned_resp = response.json()
    assert jsonned_resp["current_balance"] == 1000
    assert jsonned_resp["success"] is True
