"""test_health_check

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""

from flask import url_for
from eve import Eve
from pymongo.errors import ServerSelectionTimeoutError
import pytest
from pytest_mock.plugin import MockFixture
from mockerena.app import mongo_available


@pytest.mark.health_check
def test_health_check(client: Eve):
    """Test health check route

    :param Eve client: Mockerena app instance
    :raises: AssertionError
    """

    res = client.get(url_for('healthcheck'))
    assert res.status_code == 200
    assert res.mimetype == 'application/json'

    data = res.json
    assert data['hostname']
    assert data['status']
    assert data['timestamp']
    assert data['results']
    assert data['version']


@pytest.mark.health_check
def test_health_check_mongo_down(mocker: MockFixture):
    """Test to ensure mongo unavailability returns a down status

    :param MockFixture mocker: Mocking fixture
    :raises: AssertionError
    """

    monkey = mocker.patch('pymongo.mongo_client.MongoClient.server_info', side_effect=ServerSelectionTimeoutError())

    res = mongo_available()
    monkey.assert_called_once()
    assert res == (False, "mongo down")
