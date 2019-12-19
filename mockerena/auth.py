"""mockerena.auth

.. codeauthor John Lane <john.lane93@gmail.com>

"""

from datetime import datetime
import bcrypt
from eve.auth import BasicAuth, TokenAuth
from flask import current_app, abort, request
import jwt


def hash_password(users: list) -> list:
    """BCrypt hash password before writing to database

    :param list users: List of user objects
    :return: List of user objects
    :rtype: list
    """

    for user in users:
        user.update({'password': bcrypt.hashpw(user['password'], bcrypt.gensalt())})  # pylint: disable=no-member

    return users


def get_user(username: str, allowed_roles: list = None) -> dict:
    """Get user by username

    :param str username: User username
    :param list allowed_roles: Allowed roles
    :return: User object
    :rtype: dict
    """

    query = {'username': username}

    # Restrict access by role
    if allowed_roles:
        query['roles'] = {'$in': allowed_roles}

    users = current_app.data.driver.db['user']
    return users.find_one(query)


def get_authorized_user(allowed_roles: list = None) -> dict:
    """Get authorized user from request

    :param list allowed_roles: Allowed roles
    :return: User object
    :rtype: dict
    :raises: werkzeug.exceptions.HTTPException
    """

    # Decode web token
    try:

        token = request.headers.get('authorization').split(' ')[1]
        session = jwt.decode(token, current_app.secret_key, algorithms='HS256')
        return get_user(session['username'], allowed_roles)

    except jwt.exceptions.DecodeError:

        if not request.authorization:
            return abort(401)

        return get_user(request.authorization['username'], allowed_roles)


def compare_password(raw_password: str, password_salt: str) -> bool:
    """Compare raw password with salt hashed password

    :param str raw_password: Raw password
    :param str password_salt: Password hash
    :return: True, if the raw password matches the password salt when hashed
    :rtype: bool
    """

    return bcrypt.hashpw(raw_password, password_salt) == password_salt  # pylint: disable=no-member


class MockerenaBasicAuth(BasicAuth):
    """Mockerena basic authentication model
    """

    def check_auth(self, username: str, password: str, allowed_roles: list, resource: str, method: str) -> bool:
        """Verify user is authorized

        :param string username: Request users' username
        :param string password: Request users' password
        :param list allowed_roles: List of routes' allowed roles
        :param string resource: Resource name
        :param string method: Method name
        :return: True, if the user is authenticated and authorized
        :rtype: bool
        """

        acc = get_user(username, allowed_roles)

        # Set resource owner to authorized user
        if acc and '_id' in acc:
            self.set_request_auth_value(acc['_id'])

        return acc and compare_password(password, acc['password'])


class MockerenaTokenAuth(TokenAuth):
    """Mockerena token authentication model
    """

    def check_auth(self, token: str, allowed_roles: list, resource: str, method: str) -> bool:
        """Verify user is authorized

        :param string token: Request users' token
        :param list allowed_roles: List of routes' allowed roles
        :param string resource: Resource name
        :param string method: Method name
        :return: True, if the user is authenticated and authorized
        :rtype: bool
        """

        now = datetime.utcnow().timestamp()

        # Decode web token
        try:
            session = jwt.decode(token, current_app.secret_key, algorithms='HS256')

            acc = get_user(session['username'], allowed_roles)

            # Set resource owner to authorized user
            if acc and '_id' in acc:
                self.set_request_auth_value(acc['_id'])

            return acc and compare_password(session['password'], acc['password']) and session['exp'] > now

        except jwt.exceptions.DecodeError:

            if not request.authorization:
                return abort(401)

            acc = get_user(request.authorization['username'], allowed_roles)

            # Set resource owner to authorized user
            if acc and '_id' in acc:
                self.set_request_auth_value(acc['_id'])

            return acc and compare_password(request.authorization['password'], acc['password'])
