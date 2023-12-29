import sqlalchemy.exc as exc

from src.homework.db.crud import (
    get_user_balance_by_id,
    get_application_secret,
    delete_application,
)

from unittest.mock import patch, MagicMock


def test_get_user_balance_by_id_exception():
    with patch(
        "sqlalchemy.orm.Session.scalar",
        MagicMock(side_effect=exc.SQLAlchemyError),
    ):
        assert get_user_balance_by_id(1) is None


def test_get_application_secret():
    with patch(
        "sqlalchemy.orm.Session.scalar",
        MagicMock(side_effect=exc.SQLAlchemyError),
    ):
        assert get_application_secret("1") is None


def test_delete_application_failure():
    with patch(
        "sqlalchemy.orm.Session.execute",
        MagicMock(side_effect=exc.SQLAlchemyError),
    ), patch("sqlalchemy.orm.Session.commit", MagicMock()):
        assert delete_application("some-app-id") is False
