from unittest.mock import patch, MagicMock
from src.homework.api.user import router
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI


@pytest.fixture(name="client")
def create_test_client():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    return client


@pytest.mark.parametrize(
    "headers",
    [
        {"Not-Token": "data"},
        {"Invalid-Header": "value", "Other": "info"},
        {},
    ],
)
def test_get_balance_invalid_headers(client, headers):
    response = client.get("/user/", params={"user_id": 12345}, headers=headers)
    assert response.status_code == 401


def test_get_balance_invalid_token(client):
    with patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=False),
    ):
        response = client.get(
            "/user/", params={"user_id": 12345}, headers={"token": "invalid"}
        )
        assert response.status_code == 403


def test_get_balance_not_found(client):
    with patch(
        "src.homework.db.crud.get_user_balance_by_id",
        MagicMock(return_value=None),
    ), patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=True),
    ):
        response = client.get(
            "/user/", params={"user_id": 12345}, headers={"token": "valid"}
        )
        assert response.status_code == 404


def test_get_balance(client):
    with patch(
        "src.homework.db.crud.get_user_balance_by_id",
        MagicMock(return_value=100),
    ), patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=True),
    ):
        response = client.get(
            "/user/", params={"user_id": 12345}, headers={"token": "valid"}
        )
        assert response.status_code == 200
        assert response.json() == {"success": True, "current_balance": 100}
