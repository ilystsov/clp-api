import pytest
import sqlalchemy
from sqlalchemy.orm import Session
from src.homework.db.models import Application
from src.homework.api.security import verify_token
from func_tests.general_fixtures import (  # noqa: F401
    create_client,
    create_master_app,
    create_read_app,
    create_modify_app,
    create_db,
    insert_app,
)


@pytest.mark.parametrize("access_level", ["Can_Read", "Can_Modify_Orders"])
def test_app_creation(client, master_app, eng, access_level):
    response = client.post(
        "/application",
        headers={"token": master_app},
        json={"application_name": access_level, "access_level": access_level},
    )
    assert response.status_code == 200
    jsonned_resp = response.json()
    assert jsonned_resp.get("success")
    with Session(eng) as session:
        selectet_app = session.scalar(
            sqlalchemy.select(Application).where(
                Application.app_name == access_level
            )
        )
        assert selectet_app is not None
        assert str(selectet_app.app_id) == jsonned_resp.get("app_id")
        assert verify_token(
            jsonned_resp.get("token"), selectet_app.secret
        ) == {"app_id": jsonned_resp["app_id"], "access_level": access_level}


@pytest.mark.parametrize(
    "acces_level,created_app",
    [("Can_Read", "read_app"), ("Can_Modify_Orders", "modify_app")],
)
def test_read_to_modify(client, master_app, acces_level, created_app, request):
    created_app = request.getfixturevalue(created_app)
    response = client.put(
        "/application",
        headers={"token": master_app},
        json={
            "app_id": created_app[0],
            "new_access_level": "Can_Modify_Orders",
        },
    )
    assert response.status_code == 200
    jsonned_resp = response.json()
    assert jsonned_resp.get("success")
    assert jsonned_resp["app_id"] == created_app[0]
    assert verify_token(jsonned_resp["token"], "secret") == {
        "app_id": created_app[0],
        "access_level": "Can_Modify_Orders",
    }
