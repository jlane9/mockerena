"""test_user

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""

from flask import url_for
from eve import Eve
import pytest
import requests.auth as auth


@pytest.mark.user
@pytest.mark.post
def test_create(client: Eve):
    """Test to ensure that users can be created

    :param Eve client: Mockerena app instance
    :raises: AssertionError
    """

    acc = {
        "username": "test_username",
        "password": "test_password",
        "email": "test@email.com"
    }

    response = client.post(url_for('user|resource'), json=acc)
    assert response.status_code == 201

    data = response.json

    for item in ['_updated', '_created', '_etag', '_id', '_links', '_status']:
        assert item in data

    assert data['_status'] == 'OK'

    # Remove test artifact
    headers = {
        'If-Match': data['_etag'],
        'Authorization': auth._basic_auth_str(acc['username'], acc['password'])  # pylint: disable=protected-access
    }
    response = client.delete(url_for('account|item_lookup', _id=data['_id']), headers=headers)
    assert response.status_code == 204


@pytest.mark.user
@pytest.mark.get
def test_get_denied(client: Eve, account: dict):
    """Test to ensure that users cannot be retrieved

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': auth._basic_auth_str(  # pylint: disable=protected-access
            account['username'],
            account['password']
        )
    }

    response = client.get(url_for('user|resource'), headers=headers)
    assert response.status_code == 405


@pytest.mark.user
@pytest.mark.get
def test_get_with_id_denied(client: Eve, account: dict):
    """Test to ensure that users cannot be retrieved

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': auth._basic_auth_str(  # pylint: disable=protected-access
            account['username'],
            account['password']
        )
    }

    response = client.get(url_for('user|item_lookup', _id=account['_id']), headers=headers)
    assert response.status_code == 405


@pytest.mark.user
@pytest.mark.get
def test_get_with_username_denied(client: Eve, account: dict):
    """Test to ensure that user lookup cannot be retrieved

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': auth._basic_auth_str(  # pylint: disable=protected-access
            account['username'],
            account['password']
        )
    }

    response = client.get(url_for('user|item_lookup', _id=account['username']), headers=headers)
    assert response.status_code == 404
