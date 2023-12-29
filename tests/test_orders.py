from unittest.mock import patch, MagicMock
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.homework.api.orders import router
from src.homework.db.crud import calculate_new_points


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
@pytest.mark.parametrize("request_name", ["post", "delete"])
def test_orders_invalid_headers(client, request_name, headers):
    response = client.__getattribute__(request_name)(
        "/orders", headers=headers
    )
    assert response.status_code == 401


@pytest.mark.parametrize("request_name", ["post", "delete"])
def test_orders_invalid_token(client, request_name):
    with patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=False),
    ):
        response = client.__getattribute__(request_name)(
            "/orders", headers={"token": "invalid"}
        )
        assert response.status_code == 403


@pytest.mark.parametrize(
    "successful",
    [
        True,
        False,
    ],
)
def test_create_order(client, successful):
    with patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=True),
    ), patch(
        "src.homework.db.crud.create_order_update_balance",
        MagicMock(return_value=successful),
    ):
        response = client.post(
            "/orders",
            headers={"token": "valid"},
            json={
                "order_id": 123,
                "user_id": 456,
                "total_cost": 1000,
                "completed_at": 1630000000,
            },
        )
        assert response.status_code == 200
        assert response.json() == {"success": successful}


@pytest.mark.parametrize(
    "successful",
    [
        True,
        False,
    ],
)
def test_delete_order(client, successful):
    with patch(
        "src.homework.api.security.token_has_access",
        MagicMock(return_value=True),
    ), patch(
        "src.homework.db.crud.delete_order",
        MagicMock(return_value=successful),
    ):
        response = client.request(
            "delete",
            "/orders",
            headers={"token": "valid"},
            json={"order_id": 123},
        )
        assert response.status_code == 200
        assert response.json() == {"success": successful}


@pytest.mark.parametrize(
    "total_cost, num_of_deleted_orders, total_num_of_orders, expected_points",
    [
        (1000, 10, 50, 50),
        (2000, 0, 100, 100),
        (500, 25, 25, 5),
        (0, 5, 10, 0),
    ],
)
def test_calculate_new_points(
    total_cost, num_of_deleted_orders, total_num_of_orders, expected_points
):
    assert (
        calculate_new_points(
            total_cost, num_of_deleted_orders, total_num_of_orders
        )
        == expected_points
    )
