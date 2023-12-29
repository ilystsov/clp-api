import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from src.homework.db.models import Order, User
from src.homework.db.crud import calculate_new_points
from func_tests.test_user import insert_user  # noqa: F401
from func_tests.general_fixtures import (  # noqa: F401
    create_client,
    create_master_app,
    create_read_app,
    create_modify_app,
    create_db,
    insert_app,
)


@pytest.fixture(name="inserted_order")
def insert_order(eng, inserted_user):
    with Session(eng) as session:
        new_order = Order(
            user_id=inserted_user, total_cost=100, completed_at=1630000000
        )
        session.add(new_order)
        session.commit()
        return new_order.order_id


@pytest.mark.parametrize("req_type", ["post", "delete"])
@pytest.mark.parametrize("created_app", ["read_app", "master_app"])
def test_invalid_token(created_app, client, request, req_type):
    created_app = request.getfixturevalue(created_app)
    response = client.request(
        req_type,
        "/orders",
        headers={"token": created_app[1]},
        json={"user_id": 0, "order_id": 0, "total_cost": 0, "completed_at": 0},
    )
    assert response.status_code == 403


@pytest.mark.parametrize(
    "order_id, total_cost, completed_at",
    [(1, 300, 1630000000), (2, 500, 1630000100), (3, 1000, 1630001000)],
)
def test_order_creation(
    client, modify_app, eng, inserted_user, order_id, total_cost, completed_at
):
    with Session(eng) as session:
        user_before_order = session.scalar(
            sqlalchemy.select(User).where(User.user_id == inserted_user)
        )
        initial_balance = user_before_order.current_balance

    response = client.post(
        "/orders",
        headers={"token": modify_app[1]},
        json={
            "order_id": order_id,
            "user_id": inserted_user,
            "total_cost": total_cost,
            "completed_at": completed_at,
        },
    )
    assert response.status_code == 200
    jsonned_resp = response.json()
    assert jsonned_resp["success"] is True

    with Session(eng) as session:
        selected_order = session.scalar(
            sqlalchemy.select(Order).where(Order.order_id == order_id)
        )
        assert selected_order is not None
        assert selected_order.user_id == inserted_user
        assert selected_order.total_cost == total_cost
        assert selected_order.completed_at == completed_at

    with Session(eng) as session:
        user_after_order = session.scalar(
            sqlalchemy.select(User).where(User.user_id == inserted_user)
        )
        updated_balance = user_after_order.current_balance
        expected_new_points = calculate_new_points(
            total_cost,
            user_after_order.num_of_deleted_orders,
            len(user_after_order.orders),
        )
    assert updated_balance == initial_balance + expected_new_points


def test_delete_order(client, modify_app, eng, inserted_user, inserted_order):
    with Session(eng) as session:
        user_before_deletion = session.scalar(
            sqlalchemy.select(User).where(User.user_id == inserted_user)
        )
        initial_deleted_orders = user_before_deletion.num_of_deleted_orders

    response = client.request(
        "delete",
        "/orders",
        headers={"token": modify_app[1]},
        json={"order_id": inserted_order},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

    with Session(eng) as session:
        user_after_deletion = session.scalar(
            sqlalchemy.select(User).where(User.user_id == inserted_user)
        )
        updated_deleted_orders = user_after_deletion.num_of_deleted_orders

    assert updated_deleted_orders == initial_deleted_orders + 1
