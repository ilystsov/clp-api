import pytest
import src.homework.api.security as security


@pytest.fixture(name="token_data")
def get_data_and_precalculated_jwt():
    return (
        {
            "app_id": "test" * 9,
            "access_level": "MasterApp",
        },
        "secret",
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJhcHBfaWQiOiJ0ZXN0dGVzdHRlc3R0ZXN0dGVzdHRlc3R0ZXN0dGVzdHRlc3QiLCJhY2Nlc3NfbGV2ZWwiOiJNYXN0ZXJBcHAifQ."
        "h2gTjMWk0-5LlhWDGGUtTCGMIt-x8SRiNrCbdz5a55c",
    )


def test_issue_token(token_data):
    data, secret, result = token_data
    assert security.issue_token(data["app_id"],
                                security.MasterAccessLevel(data["access_level"]), secret) == result


def test_decode_token(token_data):
    data, secret, token = token_data
    assert security.verify_token(token, secret) == data
