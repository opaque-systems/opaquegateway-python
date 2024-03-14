"""
This module handles authentication logic for the opaqueprompts package.
"""

import os

API_KEY_ENV_VAR = "OPAQUEPROMPTS_API_KEY"


def get_api_key() -> str:
    """
    Attempts to extract the user's API key from the environment.
    Raises an error if the token is missing or empty

    Returns
    -------
    str
        The user's API key.
    """
    api_key = os.environ.get(API_KEY_ENV_VAR)
    if not api_key:
        raise Exception(
            f"Unable to get API key, \
            ensure the {API_KEY_ENV_VAR} environment variable is set."
        )
    return api_key
