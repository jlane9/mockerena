"""test_account

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""

import copy
from flask import url_for
from eve import Eve
import pytest
from tests.utils import build_basic_auth_str, create_account, delete_account, update_account


def verify_get_account_response(data: dict, account: dict):
    """Verify account get response

    :param dict data: Response data
    :param dict account: Account information
    :raises: AssertionError
    """

    for item in ['_updated', '_created', '_etag', '_id', '_links', 'username', 'email']:
        assert item in data

    assert data['_id'] == account['_id']
    assert 'password' not in data


def build_basic_auth_headers(account: dict) -> dict:
    """Build basic auth headers

    :param dict account: Account information
    :return: Basic authorization headers
    :rtype: dict
    """

    return {'Authorization': build_basic_auth_str(account)}


@pytest.mark.account
@pytest.mark.get
def test_get(client: Eve, account: dict):
    """Test to ensure account can be retrieved with basic auth

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    response = client.get(url_for('account|resource'), headers=build_basic_auth_headers(account))

    assert response.status_code == 200
    verify_get_account_response(response.json, account)


@pytest.mark.account
@pytest.mark.get
def test_get_with_id(client: Eve, account: dict):
    """Test to ensure account can be retrieved with account id

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    response = client.get(url_for('account|item_lookup', _id=account['_id']), headers=build_basic_auth_headers(account))

    assert response.status_code == 200
    verify_get_account_response(response.json, account)


@pytest.mark.account
@pytest.mark.get
def test_get_with_username(client: Eve, account: dict):
    """Test to ensure account can be retrieved with username

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    response = client.get(
        url_for('account|item_lookup', _id=account['username']),
        headers=build_basic_auth_headers(account)
    )

    assert response.status_code == 200
    verify_get_account_response(response.json, account)


@pytest.mark.account
@pytest.mark.get
def test_get_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account can be retrieved with web token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {'Authorization': f"Bearer {token_auth}"}

    response = client.get(url_for('account|resource'), headers=headers)

    assert response.status_code == 200
    verify_get_account_response(response.json, account)


@pytest.mark.account
@pytest.mark.get
def test_get_with_id_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account can be retrieved with account id and web token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {'Authorization': f"Bearer {token_auth}"}

    response = client.get(url_for('account|item_lookup', _id=account['_id']), headers=headers)

    assert response.status_code == 200
    verify_get_account_response(response.json, account)


@pytest.mark.account
@pytest.mark.get
def test_get_with_username_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account can be retrieved with username and web token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {'Authorization': f"Bearer {token_auth}"}

    response = client.get(url_for('account|item_lookup', _id=account['username']), headers=headers)

    assert response.status_code == 200
    verify_get_account_response(response.json, account)


@pytest.mark.account
@pytest.mark.get
def test_get_no_auth(client: Eve):
    """Test to ensure account can be retrieved with web token

    :param Eve client: Mockerena app instance
    :raises: AssertionError
    """

    response = client.get(url_for('account|resource'))
    assert response.status_code == 401


@pytest.mark.account
@pytest.mark.get
def test_get_with_id_no_auth(client: Eve, account: dict):
    """Test to ensure account cannot be retrieved with account id and no auth

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    response = client.get(url_for('account|item_lookup', _id=account['_id']))
    assert response.status_code == 401


@pytest.mark.account
@pytest.mark.get
def test_get_with_username_no_auth(client: Eve, account: dict):
    """Test to ensure account cannot be retrieved with username and no auth

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    response = client.get(url_for('account|item_lookup', _id=account['username']))
    assert response.status_code == 401


@pytest.mark.account
@pytest.mark.delete
def test_delete(client: Eve, account: dict):
    """Test to ensure account cannot be deleted from resource

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': build_basic_auth_str(account),
        'If-Match': account['_etag']
    }

    response = client.delete(url_for('account|resource'), headers=headers)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.delete
def test_delete_with_id(client: Eve, account: dict):
    """Test to ensure account can be deleted with account id

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': build_basic_auth_str(account),
        'If-Match': account['_etag']
    }

    response = client.delete(url_for('account|item_lookup', _id=account['_id']), headers=headers)
    assert response.status_code == 204


@pytest.mark.account
@pytest.mark.delete
def test_delete_with_username(client: Eve, account: dict):
    """Test to ensure account cannot be deleted with username

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': build_basic_auth_str(account),
        'If-Match': account['_etag']
    }

    response = client.delete(url_for('account|item_lookup', _id=account['username']), headers=headers)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.delete
def test_delete_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account cannot be deleted from resource with token

    :param Eve client: Mockerena app instance
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer {token_auth}",
        'If-Match': account['_etag']
    }

    response = client.delete(url_for('account|resource'), headers=headers)
    assert response.status_code == 405
    assert account


@pytest.mark.account
@pytest.mark.delete
def test_delete_with_id_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account can be deleted with account id and web token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer {token_auth}",
        'If-Match': account['_etag']
    }

    response = client.delete(url_for('account|item_lookup', _id=account['_id']), headers=headers)
    assert response.status_code == 204


@pytest.mark.account
@pytest.mark.delete
def test_delete_with_username_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account cannot be deleted with username and web token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer {token_auth}",
        'If-Match': account['_etag']
    }

    response = client.delete(url_for('account|item_lookup', _id=account['username']), headers=headers)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.put
def test_put(client: Eve, account: dict):
    """Test to ensure account cannot be replaced from resource

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': build_basic_auth_str(account),
        'If-Match': account['_etag']
    }

    payload = copy.deepcopy(account)
    payload['first_name'] = 'test'

    response = client.put(url_for('account|resource'), headers=headers, json=payload)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.put
def test_put_with_id(client: Eve, account: dict):
    """Test to ensure account cannot be replaced with account id

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': build_basic_auth_str(account),
        'If-Match': account['_etag']
    }

    payload = copy.deepcopy(account)
    payload['first_name'] = 'test'

    response = client.put(url_for('account|item_lookup', _id=account['_id']), headers=headers, json=payload)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.delete
def test_put_with_username(client: Eve, account: dict):
    """Test to ensure account cannot be replaced with username

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': build_basic_auth_str(account),
        'If-Match': account['_etag']
    }

    payload = copy.deepcopy(account)
    payload['first_name'] = 'test'

    response = client.put(url_for('account|item_lookup', _id=account['username']), headers=headers, json=payload)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.put
def test_put_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account cannot be replaced from resource with token

    :param Eve client: Mockerena app instance
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer {token_auth}",
        'If-Match': account['_etag']
    }

    payload = copy.deepcopy(account)
    payload['first_name'] = 'test'

    response = client.put(url_for('account|resource'), headers=headers, json=payload)
    assert response.status_code == 405
    assert account


@pytest.mark.account
@pytest.mark.put
def test_put_with_id_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account cannot be replaced with account id and web token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer {token_auth}",
        'If-Match': account['_etag']
    }

    payload = copy.deepcopy(account)
    payload['first_name'] = 'test'

    response = client.put(url_for('account|item_lookup', _id=account['_id']), headers=headers, json=payload)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.put
def test_put_with_username_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account cannot be replaced with username and web token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer {token_auth}",
        'If-Match': account['_etag']
    }

    payload = copy.deepcopy(account)
    payload['first_name'] = 'test'

    response = client.put(url_for('account|item_lookup', _id=account['username']), headers=headers, json=payload)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.patch
def test_patch(client: Eve, account: dict):
    """Test to ensure account cannot be updated from resource

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': build_basic_auth_str(account),
        'If-Match': account['_etag']
    }

    response = client.put(url_for('account|resource'), headers=headers, json={'first_name': 'test'})
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.patch
def test_patch_with_id(client: Eve, account: dict):
    """Test to ensure account can be updated with account id

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': build_basic_auth_str(account),
        'If-Match': account['_etag']
    }

    update_account(client, account, {'first_name': 'test'}, headers)


@pytest.mark.account
@pytest.mark.patch
def test_patch_with_username(client: Eve, account: dict):
    """Test to ensure account cannot be updated with username

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': build_basic_auth_str(account),
        'If-Match': account['_etag']
    }

    payload = {'first_name': 'test'}

    response = client.patch(url_for('account|item_lookup', _id=account['username']), headers=headers, json=payload)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.patch
def test_patch_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account cannot be updated from resource with token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer {token_auth}",
        'If-Match': account['_etag']
    }

    payload = {'first_name': 'test'}

    response = client.patch(url_for('account|resource'), headers=headers, json=payload)
    assert response.status_code == 405
    assert account


@pytest.mark.account
@pytest.mark.patch
def test_patch_with_id_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account can be updated with account id and web token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer {token_auth}",
        'If-Match': account['_etag']
    }

    update_account(client, account, {'first_name': 'test'}, headers)


@pytest.mark.account
@pytest.mark.patch
def test_patch_with_username_with_token(client: Eve, account: dict, token_auth: str):
    """Test to ensure account cannot be updated with username and web token

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :param str token_auth: Web token
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer {token_auth}",
        'If-Match': account['_etag']
    }

    payload = {'first_name': 'test'}

    response = client.patch(url_for('account|item_lookup', _id=account['username']), headers=headers, json=payload)
    assert response.status_code == 405


@pytest.mark.account
@pytest.mark.patch
def test_patch_unauthorized(client: Eve, account: dict):
    """Test to ensure that an account cannot update another account

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    # Create new account
    acc = {"username": "second_account", "password": "test_password", "email": "second@email.com"}
    data = create_account(client, acc)

    # Edit existing account with new account
    headers = {
        'Authorization': build_basic_auth_str(acc),
        'If-Match': account['_etag']
    }

    payload = {'settings': {'temperature_unit': 'FAHRENHEIT'}}

    response = client.patch(url_for('account|item_lookup', _id=account['_id']), headers=headers, json=payload)
    assert response.status_code == 403

    # Remove test artifact
    delete_account(client, data)


@pytest.mark.account
@pytest.mark.delete
def test_delete_unauthorized(client: Eve, account: dict):
    """Test to ensure that an account cannot delete another account

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    # Create new account
    acc = {"username": "second_account", "password": "test_password", "email": "second@email.com"}
    data = create_account(client, acc)

    # Edit existing account with new account
    headers = {
        'Authorization': build_basic_auth_str(acc),
        'If-Match': account['_etag']
    }

    response = client.delete(url_for('account|item_lookup', _id=account['_id']), headers=headers)
    assert response.status_code == 403

    # Remove test artifact
    delete_account(client, data)
