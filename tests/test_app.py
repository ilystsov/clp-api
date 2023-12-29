from unittest.mock import patch, MagicMock
import pytest

from src.homework.app import create_app


@pytest.fixture(name="app", scope="module")
def mock_app():
    with patch("src.homework.db.models.Base.metadata.create_all"), patch(
        "sqlalchemy.create_engine", return_value=MagicMock()
    ):
        return create_app()


def test_app_routes(app):
    actual_routes = set(route.path for route in app.routes)
    expected_routes = {"/application", "/user", "/orders"}
    assert expected_routes <= actual_routes
