from typing import Dict
from typing import Any

def run(user_token: str, text: str, is_prompt: bool):
    """
    Run text with an associated user token through the Gateway.
    
    Parameters
    ----------
    user_token : str
        User's JWT token
    text : str
        Either the model prompt or response
    is_prompt: bool
        If true, the text is a prompt. Otherwise, the text is a model response.
        The Gateway will evaluate the text depending on whether it's a prompt
        or response.
        
    Returns
    -------
    evaluated_text : str
        The text evaluated by the Gateway.
    """
    pass

