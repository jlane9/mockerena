"""Definition for mockerena user

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""


from flask import abort
from mockerena.auth import MockerenaTokenAuth, get_authorized_user
from mockerena.models.common import STRING, UNIQUE_STRING, to_lower


USER_SCHEMA = {
    "email": {**UNIQUE_STRING, "coerce": to_lower},
    "first_name": STRING,
    "last_name": STRING,
    "password": {**STRING, "required": True},
    "username": {**UNIQUE_STRING, "coerce": to_lower}
}

USER = {
    "datasource": {
        "projection": {item: 1 for item in USER_SCHEMA if item not in ("password", "roles")}
    },
    "item_methods": [],
    "item_title": "user",
    "public_methods": ["POST"],
    "resource_methods": ["POST"],
    "schema": USER_SCHEMA
}

ACCOUNT = {
    "additional_lookup": {
        "url": "regex('[\\w]+')",
        "field": "username"
    },
    "authentication": MockerenaTokenAuth,
    "datasource": {
        "source": "user",
        "projection": {item: 1 for item in USER_SCHEMA if item not in ("password", "roles")}
    },
    "item_methods": ["GET", "PATCH", "DELETE"],
    "item_title": "account",
    "resource_methods": ["GET"],
    "schema": USER_SCHEMA
}


def default_current_user(_, lookup: dict):
    """Default search to current user

    :param _: Flask request
    :param dict lookup: Lookup payload
    """

    lookup['_id'] = str(get_authorized_user()['_id'])


def verify_is_user(_, lookup: dict):
    """Verify this is the user's account

    :param _: Eve request
    :param dict lookup: Account payload
    :raises: werkzeug.exceptions.HTTPException
    """

    if not lookup:
        return

    account = get_authorized_user()

    if 'username' in lookup and str(account['username']) != str(lookup['username']):
        abort(403)

    elif '_id' in lookup and str(account['_id']) != str(lookup['_id']):
        abort(403)
