from sqlalchemy import select
from sqlalchemy.orm import Session
import sqlalchemy.exc as exc
from src.homework.db.models import Application
from src.homework.db.engine import engine


def get_app_by_id(app_id: str) -> None | Application:
    """
    Get an application from the database by its id.

    If the application with given id does not exist, function returns None.
    :param app_id: str
    :return: None | Application
    """
    with Session(engine) as session:
        app = session.scalar(
            select(Application).where(Application.app_id == app_id)
        )
        return app


def create_application(app_id: str, app_name: str, secret: str) -> bool:
    try:
        new_application = Application(
            app_id=app_id,
            app_name=app_name,
            secret=secret,
        )
        with Session(engine) as session:
            session.add(new_application)
            session.commit()
    except (exc.SQLAlchemyError, exc.DBAPIError):
        return False
    return True
