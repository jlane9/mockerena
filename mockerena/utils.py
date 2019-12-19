"""Common utility methods

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""


import json
from flask.wrappers import Response
from werkzeug.local import LocalProxy


def return_one(_: str, payload: Response):
    """Alter eve response to return the first item

    :param _: Flask request
    :param Response payload: Response payload
    """

    if isinstance(payload.json, dict) and '_items' in payload.json:
        payload.set_data(json.dumps(payload.json['_items'][0]))


def strip_creator(_: str, request: LocalProxy):
    """Remove creator from object

    :param str _: Eve resource name
    :param LocalProxy request: Eve request
    """

    if isinstance(request.view_args, dict):
        request.view_args.pop('creator', None)
