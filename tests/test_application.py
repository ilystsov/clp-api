from unittest.mock import patch, MagicMock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.homework.api.application import router


@pytest.fixture(name="client")
def create_test_client():
    app = FastAPI()
    app.include_router(router)
    client = TestClient(app)
    return client


@pytest.mark.parametrize("request_name", ["post", "put", "delete"])
def test_update_app_without_headers(client, request_name):
    response = client.__getattribute__(request_name)("/application")
    assert response.status_code == 401


@pytest.mark.parametrize("request_name", ["post", "put", "delete"])
def test_update_app_with_invalid_token(client, request_name):
    with patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=False),
    ):
        response = client.__getattribute__(request_name)(
            "/application", headers={"token": "test"}
        )
        assert response.status_code == 403


@pytest.mark.parametrize(
    "test_case",
    [
        ("Can_Read", True, ["app_id", "token", "success"]),
        ("Can_Read", False, ["success"]),
        ("Can_Modify_Orders", True, ["app_id", "token", "success"]),
        ("Can_Modify_Orders", False, ["success"]),
    ],
)
def test_create_app(client, test_case):
    with patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=True),
    ), patch(
        "src.homework.db.crud.create_application",
        MagicMock(return_value=test_case[1]),
    ):
        response = client.post(
            "/application",
            headers={"token": "test"},
            json={
                "application_name": "test",
                "access_level": test_case[0],
            },
        )
        assert response.status_code == 200
        assert all(resp in response.json() for resp in test_case[2])
        assert len(response.json()) == len(test_case[2])


@pytest.mark.parametrize(
    "test_case",
    [
        ("Can_Read", "secret", ["app_id", "token", "success"]),
        ("Can_Read", None, ["success"]),
        ("Can_Modify_Orders", "secret", ["app_id", "token", "success"]),
        ("Can_Modify_Orders", None, ["success"]),
    ],
)
def test_update_app(client, test_case):
    with patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=True),
    ), patch(
        "src.homework.db.crud.get_application_secret",
        MagicMock(return_value=test_case[1]),
    ):
        response = client.put(
            "/application",
            headers={"token": "test"},
            json={"app_id": "test", "new_access_level": test_case[0]},
        )
        assert response.status_code == 200
        assert all(resp in response.json() for resp in test_case[2])
        assert len(response.json()) == len(test_case[2])


@pytest.mark.parametrize(
    "successful",
    [
        True,
        False,
    ],
)
def test_delete_app(client, successful):
    with patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=True),
    ), patch(
        "src.homework.db.crud.delete_application",
        MagicMock(return_value=successful),
    ):
        response = client.request(
            "delete",
            "/application",
            headers={"token": "test"},
            json={"app_id": "test"},
        )
        assert response.status_code == 200
        assert response.json() == {"success": successful}
