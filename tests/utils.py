"""test utils

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""


from flask import url_for
from eve import Eve
from pytest_flask.plugin import JSONResponse
import requests.auth as auth


def build_basic_auth_str(acc: dict) -> str:
    """Builds basic auth string

    :param dict acc: User information
    :return: Basic auth string
    :rtype: str
    """

    return auth._basic_auth_str(acc.get('username'), acc.get('password'))  # pylint: disable=protected-access


def create_account(api: Eve, acc: dict):
    """Create a user account

    :param Eve api: Mockerena app instance
    :param dict acc: User information
    :return:
    """

    response = api.post(url_for('user|resource'), json=acc)
    assert response.status_code == 201
    return {**response.json, **acc}


def delete_account(api: Eve, acc: dict):
    """Delete user account

    :param Eve api: Mockerena app instance
    :param dict acc: User information
    :raises: AssertionError
    """

    headers = {
        'If-Match': acc['_etag'],
        'Authorization': build_basic_auth_str(acc)
    }
    response = api.delete(url_for('account|item_lookup', _id=acc['_id']), headers=headers)
    assert response.status_code == 204


def update_account(api: Eve, account: dict, payload: dict, headers: dict) -> JSONResponse:
    """Update user account

    :param Eve api: Mockerena app instance
    :param dict account: User information
    :param dict payload: Values to update
    :param dict headers: Request headers
    :return: Delete response
    :rtype: JSONResponse
    """

    response = api.patch(url_for('account|item_lookup', _id=account['_id']), headers=headers, json=payload)
    assert response.status_code == 200

    return response
