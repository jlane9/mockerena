"""Common definitions between models

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""


# PRIMITIVE MODELS
BOOLEAN = {
    "type": "boolean"
}


DATETIME = {
    "type": "datetime"
}


FLOAT = {
    "type": "float"
}


INTEGER = {
    "type": "integer"
}


LIST = {
    "type": "list"
}


STRING = {
    "type": "string"
}


# COMPLEX MODELS
EMAIL = {
    **STRING,
    "maxlength": 1024
}


POSITIVE_INTEGER = {
    **INTEGER,
    "min": 0
}


UNIQUE_STRING = {
    **STRING,
    "required": True,
    "unique": True
}


URL = {
    **STRING,
    "maxlength": 1024
}


# RELATIONAL MODELS
USER = {
    "type": "objectid",
    "readonly": True,
    "data_relation": {
        "resource": "user",
        "field": "_id",
        "embeddable": True
    }
}


# METHODS
def to_lower(value: str) -> str:
    """Coerce value to lowercase

    :param str value: Value to coerce
    :return: Sting lower-cased
    :rtype: str
    """

    return str(value).lower()


def to_upper(value: str) -> str:
    """Coerce value to uppercase

    :param str value: Value to coerce
    :return: String upper-cased
    :rtype: str
    """

    return str(value).upper()
