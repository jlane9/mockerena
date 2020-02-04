"""conftest.py

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""

from copy import deepcopy
from flask import url_for
from eve import Eve
import pytest
from requests.auth import _basic_auth_str
from mockerena.app import app as server
from tests.utils import build_basic_auth_str


MOCK_SCHEMA = {
    "schema": "mock_example",
    "num_rows": 10,
    "file_format": "csv",
    "file_name": "mock_{}_example",
    "columns": [
        {
            "name": "foo",
            "type": "random_element",
            "args": {
                "elements": ["this"]
            }
        },
        {
            "name": "bar",
            "type": "random_element",
            "args": {
                "elements": ["that"]
            }
        }
    ]
}


@pytest.fixture(scope="session")
def app() -> Eve:
    """Returns mockerena app instance as a test fixture

    :return: An Eve application
    :rtype: Eve
    """

    return server


@pytest.fixture()
def sample_schema() -> dict:
    """Returns sample schema for mockerena

    :return: An example schema
    :rtype: dict
    """

    return deepcopy(MOCK_SCHEMA)


@pytest.fixture(scope="function")
def account(client: Eve) -> dict:
    """Create an account for test

    :param Eve client: Mockerena app instance
    :return: Account information
    :rtype: dict
    """

    user = {
        "username": "mock_username",
        "password": "mock_password",
        "email": "mock@email.com"
    }

    response = client.post(url_for('user|resource'), json=user)

    if response.status_code != 422:
        assert response.status_code == 201
    else:
        headers = {'Authorization': build_basic_auth_str(user)}
        response = client.get(url_for('account|resource'), headers=headers)

    data = response.json

    yield {**data, **user}

    # Make sure user still exists
    headers = {'Authorization': build_basic_auth_str(user)}
    response = client.get(url_for('account|item_lookup', _id=data['_id']), headers=headers)

    if response.status_code not in (401, 404):

        # Remove user's schema
        if client.get(url_for('schema|item_lookup', _id='mock_example'), headers=headers).status_code == 200:
            client.delete(url_for('schema|item_lookup', _id='mock_example'), headers=headers)

        # Remove user
        data = response.json
        headers['If-Match'] = data['_etag']
        response = client.delete(url_for('account|item_lookup', _id=data['_id']), headers=headers)
        assert response.status_code == 204


@pytest.fixture(autouse=True)
def setup_data(client: Eve, account: dict):  # pylint:disable=redefined-outer-name
    """Setup example schema for testing

    :param Eve client: Mockerena app instance
    :param dict account: Account information
    """

    data = deepcopy(MOCK_SCHEMA)

    headers = {
        'Authorization': build_basic_auth_str(account),
        'Content-Type': 'application/json'
    }

    # Setup
    if not client.get(url_for('schema|item_lookup', _id='mock_example'), headers=headers).status_code == 200:
        client.post(url_for('schema|resource'), json=data, headers=headers)


@pytest.fixture(scope="function")
def token_auth(client: Eve) -> str:
    """Generate JSON web token

    :param Eve client: Mockerena app instance
    :return: JSON web token
    :rtype: str
    """

    headers = {'Authorization': _basic_auth_str("mock_username", "mock_password")}
    response = client.post(url_for('secure'), headers=headers)

    assert response.status_code == 201
    yield response.data.decode("utf-8")
