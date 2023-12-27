import typing

import sqlalchemy
import sqlalchemy.orm as orm


class Base(orm.DeclarativeBase):
    pass


class Application(Base):
    __tablename__ = "applications"
    app_id: orm.Mapped[sqlalchemy.UUID] = orm.mapped_column(
        sqlalchemy.UUID(as_uuid=True), primary_key=True
    )
    app_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(30))
    token: orm.Mapped[str] = orm.mapped_column(sqlalchemy.Text)


class User(Base):
    __tablename__ = "users"
    user_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer, primary_key=True
    )
    current_balance: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
    num_of_deleted_orders: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer
    )
    orders: orm.Mapped[typing.List["Order"]] = orm.relationship()


class Order(Base):
    __tablename__ = "orders"
    order_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer, primary_key=True
    )
    user_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.ForeignKey("users.user_id")
    )
    total_cost: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
    completed_at: orm.Mapped[int] = orm.mapped_column(sqlalchemy.Integer)
