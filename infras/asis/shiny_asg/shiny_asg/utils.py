
from typing import Union


def obtain_config(app, key_name: str) -> dict:
    return app.node.try_get_context(key_name)
