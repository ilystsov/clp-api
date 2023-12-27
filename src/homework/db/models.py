import typing

import sqlalchemy
import sqlalchemy.orm as orm


class Base(orm.DeclarativeBase):
    pass


class Applications(Base):
    __tablename__ = "applications"
    app_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.UUID, primary_key=True
    )
    app_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(30))
    token: orm.Mapped[str] = orm.mapped_column(sqlalchemy.Text)


class Users(Base):
    __tablename__ = "users"
    user_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer, primary_key=True
    )
    current_balance: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
    num_of_deleted_orders: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer
    )
    orders: orm.Mapped[typing.List["Orders"]] = orm.relationship()


class Orders(Base):
    __tablename__ = "orders"
    order_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer, primary_key=True
    )
    user_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey("users.user_id")
    )
    total_cost: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
    completed_ar: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
