import typing
import enum
import jwt
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from src.homework.api.contracts import AccessLevel
from src.homework.db.engine import get_postgres_db_url
from src.homework.db.models import Application


class MasterAccessLevel(enum.Enum):
    MASTER_APP = "MasterApp"


BroadenAccessLevel = typing.Union[AccessLevel, MasterAccessLevel]


def issue_token(
    app_id: str, access_level: BroadenAccessLevel, secret: str
) -> str:
    return jwt.encode(
        {"app_id": app_id, "access_level": access_level.value},
        secret,
        algorithm="HS256",
    )


def verify_token(token: str, supposed_secret: str) -> typing.Dict[str, str]:
    return jwt.decode(token, supposed_secret, algorithms="HS256")


def get_secret_by_app_id(app_id: str, get_url_func: typing.Callable[[], str]) -> None | Application:
    engine = create_engine(get_url_func())
    with Session(engine) as session:
        app = session.scalar(select(Application).where(Application.app_id == app_id))
        return app
