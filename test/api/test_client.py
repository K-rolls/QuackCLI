import pytest
from unittest.mock import patch, ANY
from src.api.api_client import APIClient


@pytest.fixture
def mock_password_handler():
    with patch("src.api.api_client.PasswordHandler") as mock:
        yield mock.return_value


@pytest.fixture
def api_client(mock_password_handler):
    with patch("src.api.api_client.requests.Session") as mock_session:
        client = APIClient()
        client.session = mock_session.return_value
        yield client


def test_make_request_with_api_key(api_client):
    api_client.api_key = "test_api_key"
    api_client.session.request.return_value.json.return_value = {"data": "test"}

    result = api_client._make_request("GET", "test_endpoint")

    api_client.session.request.assert_called_once_with(
        "GET",
        f"{api_client.base_url}/test_endpoint",
        json=None,
        data=None,
        params=None,
        files=None,
        headers={"X-API-Key": "test_api_key"},
    )
    assert result == {"data": "test"}


def test_make_request_with_access_token(api_client):
    api_client.api_key = None
    api_client.access_token = "test_access_token"
    api_client.session.request.return_value.json.return_value = {"data": "test"}

    result = api_client._make_request("POST", "test_endpoint", data={"key": "value"})

    api_client.session.request.assert_called_once_with(
        "POST",
        f"{api_client.base_url}/test_endpoint",
        json={"key": "value"},
        data=None,
        params=None,
        files=None,
        headers={"Authorization": "Bearer test_access_token"},
    )
    assert result == {"data": "test"}


def test_set_access_token(api_client, mock_password_handler):
    api_client.set_access_token("new_token")
    assert api_client.access_token == "new_token"
    mock_password_handler.set_password.assert_called_once_with(
        "access_token", "new_token"
    )


def test_clear_access_token(api_client, mock_password_handler):
    api_client.access_token = "token"
    mock_password_handler.get_password.return_value = "token"
    mock_password_handler.delete_password.return_value = True

    result = api_client.clear_access_token()

    assert result is True
    assert api_client.access_token is None
    mock_password_handler.delete_password.assert_called_once_with("access_token")


def test_set_api_key(api_client, mock_password_handler):
    api_client.set_api_key("new_api_key")
    assert api_client.api_key == "new_api_key"
    mock_password_handler.set_password.assert_called_once_with("api_key", "new_api_key")


def test_clear_api_key(api_client, mock_password_handler):
    api_client.api_key = "key"
    mock_password_handler.get_password.return_value = "key"
    mock_password_handler.delete_password.return_value = True

    result = api_client.clear_api_key()

    assert result is True
    assert api_client.api_key is None
    mock_password_handler.delete_password.assert_called_once_with("api_key")


def test_get_method(api_client):
    api_client.session.request.return_value.json.return_value = {"data": "get_test"}
    result = api_client.get(
        "test_endpoint", params={"param": "value"}, headers={"Custom-Header": "Value"}
    )
    api_client.session.request.assert_called_once_with(
        "GET",
        f"{api_client.base_url}/test_endpoint",
        json=None,
        data=None,
        params={"param": "value"},
        headers={"Custom-Header": "Value", "X-API-Key": ANY},
        files=None,
    )
    assert result == {"data": "get_test"}


def test_post_method(api_client):
    api_client.session.request.return_value.json.return_value = {"data": "post_test"}
    result = api_client.post("test_endpoint", data={"key": "value"})
    api_client.session.request.assert_called_once_with(
        "POST",
        f"{api_client.base_url}/test_endpoint",
        json={"key": "value"},
        data=None,
        params=None,
        headers={"X-API-Key": ANY},
        files=None,
    )
    assert result == {"data": "post_test"}


def test_put_method(api_client):
    api_client.session.request.return_value.json.return_value = {"data": "put_test"}
    result = api_client.put("test_endpoint", data={"key": "value"})
    api_client.session.request.assert_called_once_with(
        "PUT",
        f"{api_client.base_url}/test_endpoint",
        json={"key": "value"},
        data=None,
        params=None,
        headers={"X-API-Key": ANY},
        files=None,
    )
    assert result == {"data": "put_test"}


def test_delete_method(api_client):
    api_client.session.request.return_value.json.return_value = {"data": "delete_test"}
    result = api_client.delete("test_endpoint")
    api_client.session.request.assert_called_once_with(
        "DELETE",
        f"{api_client.base_url}/test_endpoint",
        json=None,
        data=None,
        params=None,
        headers={"X-API-Key": ANY},
        files=None,
    )
    assert result == {"data": "delete_test"}


def test_clear_access_token_returns_false_when_no_token(
    api_client, mock_password_handler
):
    api_client.access_token = None
    mock_password_handler.get_password.return_value = None

    result = api_client.clear_access_token()

    assert result is False
    mock_password_handler.delete_password.assert_not_called()


def test_clear_api_key_returns_false_when_no_key(api_client, mock_password_handler):
    api_client.api_key = None
    mock_password_handler.get_password.return_value = None

    result = api_client.clear_api_key()

    assert result is False
    mock_password_handler.delete_password.assert_not_called()
