"""test_auth

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""

from flask import url_for
import pytest
import requests.auth as auth


@pytest.mark.auth
@pytest.mark.post
def test_get_token_auth(client, account):
    """Test to ensure token auth can be generated

    :param Flask client: Mockerena app instance
    :param dict account: Account information
    :raises: AssertionError
    """

    headers = {
        'Authorization': auth._basic_auth_str(  # pylint: disable=protected-access
            account['username'],
            account['password']
        )
    }

    response = client.post(url_for('secure'), headers=headers)
    assert response.status_code == 201
    assert response.data


@pytest.mark.auth
@pytest.mark.post
def test_get_token_auth_unauthorized(client):
    """Test to ensure an unauthorized user cannot generate a token auth

    :param Flask client: Mockerena app instance
    :raises: AssertionError
    """

    headers = {
        'Authorization': auth._basic_auth_str('user', 'unknown')  # pylint: disable=protected-access
    }

    response = client.post(url_for('secure'), headers=headers)
    assert response.status_code == 401


@pytest.mark.auth
@pytest.mark.post
def test_get_token_no_auth(client):
    """Test to ensure a user cannot generate a token without auth

    :param Flask client: Mockerena app instance
    :raises: AssertionError
    """

    response = client.post(url_for('secure'))
    assert response.status_code == 401


@pytest.mark.auth
@pytest.mark.get
def test_malformed_token(client):
    """Test to ensure malformed tokens return unauthorized

    :param Flask client: Mockerena app instance
    :raises: AssertionError
    """

    headers = {
        'Authorization': f"Bearer malformed"
    }

    response = client.get(url_for('account|resource'), headers=headers)
    assert response.status_code == 401
