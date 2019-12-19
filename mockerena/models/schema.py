"""Definition for mockerena schema

.. codeauthor:: John Lane <john.lane93@gmail.com>

"""

from copy import deepcopy
from mockerena.auth import MockerenaTokenAuth
from mockerena.models.common import BOOLEAN, STRING


SCHEMA = {
    "auth_field": "creator",
    "authentication": MockerenaTokenAuth,
    "item_title": "schema",
    "schema": {
        "schema": {
            "type": "string",
            "minlength": 3,
            "maxlength": 64,
            "unique": True,
            "required": True
        },
        "num_rows": {
            "type": "integer",
            "min": 1,
            "default": 1000
        },
        "file_format": {
            "type": "string",
            "required": True
        },
        "file_name": {
            "type": "string",
            "minlength": 3,
            "maxlength": 64
        },
        "include_header": BOOLEAN,
        "exclude_null": BOOLEAN,
        "is_nested": BOOLEAN,
        "delimiter": STRING,
        "key_separator": STRING,
        "quote_character": STRING,
        "template": STRING,
        "root_node": STRING,
        "table_name": STRING,
        "columns": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "type": STRING,
                    "name": STRING,
                    "format": STRING,
                    "args": {"type": "dict"},
                    "percent_empty": {
                        "type": "float",
                        "min": 0,
                        "max": 1
                    },
                    "truncate": BOOLEAN,
                    "function": STRING,
                    "description": STRING
                }
            }
        },
        "responses": {
            "type": "list",
            "items": [
                {
                    "type": "dict",
                    "schema": {
                        "status_code": {
                            "type": "integer",
                            "min": 100,
                            "max": 599
                        },
                        "headers": {"type": "dict", "allow_unknown": True},
                        "content_type": {"type": "string"},
                        "data": {"type": "string"},
                        "weight": {
                            "type": "integer",
                            "min": 1
                        }
                    }
                }
            ]
        }
    },
    "additional_lookup": {
        "url": 'regex("[\\w]+")',
        "field": "schema"
    },
}

# Build a schema for custom_schema route
CUSTOM_SCHEMA = deepcopy(SCHEMA["schema"])
del CUSTOM_SCHEMA["schema"]["unique"]
