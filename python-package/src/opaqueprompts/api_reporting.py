from typing import Dict
from typing import Any

###########
# Reporting
###########
def get_total_input_tokens():
    """
    Count the total number of tokens passed through the Gateway.

    Returns
    -------
    total_tokens : int
        The total number of tokens processed.
    """
    pass

def get_total_input_tokens_by_user(user_id: str):
    """
    Count the total number of tokens a specific user has pushed through the Gateway.

    Parameters
    ----------
    user_id : str
        The unique identifier for the user.

    Returns
    -------
    user_tokens : int
        The total number of tokens pushed through by the specified user.
    """
    pass

def get_total_input_tokens_by_role(role_id: str):
    """
    Count the total number of tokens a specific role has pushed through the Gateway.

    Parameters
    ----------
    role_id : str
        The unique identifier for the role.

    Returns
    -------
    role_tokens : int
        The total number of tokens pushed through by the specified role.
    """
    pass

def get_total_input_requests():
    """
    Count the total number of requests passed through the Gateway.

    Returns
    -------
    total_requests : int
        The total number of requests processed.
    """
    pass

def get_total_input_requests_by_role(role_id: str):
    """
    Count the total number of requests a specific role has made to the Gateway.

    Parameters
    ----------
    role_id : str
        The unique identifier for the role.

    Returns
    -------
    role_requests : int
        The total number of requests made by the specified role.
    """
    pass

def get_total_input_requests_by_user(user_id: str):
    """
    Count the total number of requests a specific user has made to the Gateway.

    Parameters
    ----------
    user_id : str
        The unique identifier for the user.

    Returns
    -------
    user_requests : int
        The total number of requests made by the specified user.
    """
    pass
