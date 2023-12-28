from sqlalchemy import select, delete
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
    """
    Create an application in the database.

    :param app_id: uuid 4 format string
    :param app_name: 30-character length string
    :param secret: 64-character length string
    :return: bool indicating success of creation
    """
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


def get_application_secret(app_id: str) -> None | str:
    """
    Get a secret if app exists, and None otherwise.

    :param app_id: uuid 4 format string
    :return: None | 64-character string
    """
    try:
        with Session(engine) as session:
            app = session.scalar(
                select(Application).where(Application.app_id == app_id)
            )
            if app is None:
                return None
            return app.secret
    except (exc.SQLAlchemyError, exc.DBAPIError):
        return None


def delete_application(app_id: str) -> bool:
    """
    Delete an app and get result of the operation.

    :param app_id: uuid 4 format string
    :return: bool indicating operation's result
    """
    try:
        with Session(engine) as session:
            session.execute(
                delete(Application).where(Application.app_id == app_id)
            )
            session.commit()
    except (exc.SQLAlchemyError, exc.DBAPIError):
        return False
    return True
