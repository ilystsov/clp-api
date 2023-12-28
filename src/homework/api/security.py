import binascii
import typing
import enum
import jwt
import base64
import json

from fastapi import Header, HTTPException

from src.homework.api.contracts import AccessLevel
from src.homework.db.crud import get_app_by_id


class MasterAccessLevel(enum.Enum):
    MASTER_APP = "MasterApp"


BroadenAccessLevel = typing.Union[AccessLevel, MasterAccessLevel]


def issue_token(
    app_id: str, access_level: BroadenAccessLevel, secret: str
) -> str:
    """
    Generate a token signed by secret.

    :param app_id: str
    :param access_level: BroadenAccessLevel
    :param secret: str
    :return: str
    """
    return jwt.encode(
        {"app_id": app_id, "access_level": access_level.value},
        secret,
        algorithm="HS256",
    )


def verify_token(token: str, supposed_secret: str) -> dict[str, str]:
    return jwt.decode(token, supposed_secret, algorithms="HS256")


def decode_segment(segment: str) -> None | dict[str, str]:
    """
    Decode a given segment of the JWT.

    :param segment: str
    :return: decoded JWT - dict
    """
    try:
        binary_decoded = base64.b64decode(segment + "==")
        jsonned_data = json.loads(binary_decoded.decode())
    except (binascii.Error, json.JSONDecodeError, UnicodeDecodeError):
        return None
    return jsonned_data


def token_has_access(token: str, access_level: BroadenAccessLevel) -> bool:
    """
    Verify that the token has required access level.

    The function is expected to be used for the FastApi header check.
    :param token: str
    :param access_level: BroadenAccessLevel
    :return: bool
    """
    try:
        payload = decode_segment(token.split(".")[1])
    except IndexError:
        return False
    if payload is None or payload.get("app_id") is None:
        return False
    app = get_app_by_id(payload.get("app_id"))
    if app is None:
        return False
    try:
        decoded_payload = verify_token(token, app.secret)
    except jwt.PyJWTError:
        return False
    return decoded_payload["access_level"] == access_level.value


class ValidateHeader:
    """
    Validate Header with an instance of a class.
    use case:
    https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/
    Specify security level for a router:
    >>> from fastapi import APIRouter, Depends
    >>> read_only_access_level = AccessLevel("Can_Read")
    >>> router = APIRouter(
    >>>     prefix="/items",
    >>>     tags=["items"],
    >>>     dependencies=[Depends(ValidateHeader(read_only_access_level))],
    >>>     responses={404: {"description": "Not found"}},
    >>>     )

    TODO: HTTPException response schema does not match specification,
        it returns {"detail": ...} json instead of {"success": False}
        (priority - low)
    """

    def __init__(self, required_access_level: BroadenAccessLevel):
        self.required_access_level = required_access_level

    async def __call__(
        self, token: typing.Annotated[str | None, Header()] = None
    ):
        if token is None:
            raise HTTPException(status_code=401)
        if not token_has_access(token, self.required_access_level):
            raise HTTPException(status_code=403)
