"""
This module handles authentication logic for the promptguard package.
"""
import os


ACCESS_TOKEN_ENV_VAR = "PROMPT_GUARD_ACCESS_TOKEN"

def get_access_token() -> str:
    """
    Attempts to extract the users access token from the environment.
    Raises an error if the token is missing or empty

    Returns
    -------
    str
        The users access token
    """
    access_token = os.environ.get(ACCESS_TOKEN_ENV_VAR)
    if not access_token:
        raise Exception(f"Unable to get access token, ensure the {ACCESS_TOKEN_ENV_VAR} is set.")
    return access_token
