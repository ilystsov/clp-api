from unittest.mock import patch
import pytest
import src.homework.api.security as security
from src.homework.api.contracts import AccessLevel
from src.homework.db.models import Application


@pytest.fixture(name="token_data")
def get_data_and_precalculated_jwt():
    return (
        {
            "app_id": "test" * 9,
            "access_level": "MasterApp",
        },
        "secret",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJhcHBfaWQiOiJ0ZXN0dGVzdHRlc3R0ZXN0dGVzdH"
        "Rlc3R0ZXN0dGVzdHRlc3QiLCJhY2Nlc3NfbGV2ZWwiOiJNYXN0ZXJBcHAifQ."
        "h2gTjMWk0-5LlhWDGGUtTCGMIt-x8SRiNrCbdz5a55c",
    )


def test_issue_token(token_data):
    data, secret, result = token_data
    assert (
            security.issue_token(
                data["app_id"],
                security.MasterAccessLevel(data["access_level"]),
                secret,
            )
            == result
    )


def test_decode_token(token_data):
    data, secret, token = token_data
    assert security.verify_token(token, secret) == data


def test_decode_segment(token_data):
    data, _, token = token_data
    assert security.decode_segment(token.split(".")[1]) == data


@pytest.mark.parametrize(
    "test_case",
    [
        (security.MasterAccessLevel("MasterApp"), "secret", True),
        (AccessLevel("Can_Read"), "secret", False),
        (AccessLevel("Can_Modify_Orders"), "secret", False),
        (security.MasterAccessLevel("MasterApp"), "nesecret", False),
    ],
)
def test_token_has_access(token_data, test_case):
    _, __, token = token_data
    with patch(
            "src.homework.api.security.get_app_by_id",
            lambda x: Application(
                app_id="test" * 9, app_name="test", secret=test_case[1]
            ),
    ):
        assert security.token_has_access(token, test_case[0]) == test_case[2]


@patch("src.homework.api.security.get_app_by_id", lambda x: None)
def test_bad_token():
    assert not security.token_has_access("test", security.MasterAccessLevel("MasterApp"))
    assert not security.token_has_access("test.test.", security.MasterAccessLevel("MasterApp"))
