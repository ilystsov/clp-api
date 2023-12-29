from sqlalchemy import select, delete
from sqlalchemy.orm import Session
import sqlalchemy.exc as exc
from src.homework.db.models import Application, User, Order
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


def get_user_balance_by_id(user_id: int) -> None | int:
    """
    Get the user's balance from the database by their id.

    If the user with given user_id does not exist, function returns None.
    :param user_id: int
    :return: None | int
    """
    with Session(engine) as session:
        try:
            balance = session.scalar(
                select(User.current_balance).where(User.user_id == user_id)
            )
            return balance
        except (exc.SQLAlchemyError, exc.DBAPIError):
            return None


def calculate_new_points(
    total_cost: int, num_of_deleted_orders: int, total_num_of_orders: int
) -> int:
    """
    Calculate the number of additional points.

    :param total_cost: int
    :param num_of_deleted_orders: int
    :param total_num_of_orders: int
    :return: int
    """
    normal_coef = min(
        1, 1.2 - num_of_deleted_orders / (total_num_of_orders + 1)
    )
    new_points = total_cost * 0.05 * normal_coef
    return int(new_points)


def create_order_update_balance(
    order_id: int, user_id: int, total_cost: int, completed_at: int
) -> bool:
    """
    Create a new order entry in the database
    and update user's balance.

    :param order_id: int
    :param user_id: int
    :param total_cost: int
    :param completed_at: int
    :return: bool indicating operation's result
    """
    try:
        new_order = Order(
            order_id=order_id,
            user_id=user_id,
            total_cost=total_cost,
            completed_at=completed_at,
        )
        with Session(engine) as session:
            session.add(new_order)
            session.commit()

        with Session(engine) as session:
            user = session.scalar(select(User).where(User.user_id == user_id))
            total_num_of_orders = len(user.orders)
            num_of_deleted_orders = user.num_of_deleted_orders

            new_points = calculate_new_points(
                total_cost, num_of_deleted_orders, total_num_of_orders
            )
            user.current_balance += new_points
            session.commit()
    except (exc.SQLAlchemyError, exc.DBAPIError):
        return False
    return True


def delete_order(order_id: int) -> bool:
    """
    Delete an order and get result of the operation.

    :param order_id: int
    :return: bool indicating operation's result
    """
    try:
        with Session(engine) as session:
            order = session.scalar(
                select(Order).where(Order.order_id == order_id)
            )
            user = session.scalar(
                select(User).where(User.user_id == order.user_id)
            )

            session.delete(order)
            user.num_of_deleted_orders += 1

            session.commit()
    except (exc.SQLAlchemyError, exc.DBAPIError):
        return False
    return True
