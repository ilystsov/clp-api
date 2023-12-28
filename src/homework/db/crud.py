import typing

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.homework.db.models import Application


def get_app_by_id(
    app_id: str, get_url_func: typing.Callable[[], str]
) -> None | Application:
    """
    Get an application from the database by its id.

    If the application with given id does not exist, function returns None.
    :param app_id: str
    :param get_url_func: a function to generate connection string
    :return: None | Application
    """
    engine = create_engine(get_url_func())
    with Session(engine) as session:
        app = session.scalar(
            select(Application).where(Application.app_id == app_id)
        )
        return app
