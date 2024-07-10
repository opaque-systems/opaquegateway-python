from typing import Any, Dict, List

############
# Guardrails
############
def add_guardrail(guardrail: str, guardrail_type: str, config: Any):
    """
    Add a guardrail.

    Parameters
    ----------
    guardrail : str
        The name of the guardrail to add.
    guardrail_type : str
        The type of guardrail to add. One of: vulnerability, input, dialog, retrieval, execution, output.
    config : Any
        The configuration details for the guardrail.
    """
    pass

def set_vulnerability_guardrails(guardrails: Dict[str, str]):
    """
    Set the vulnerability guardrails to enable.

    Parameters
    ----------
    guardrails : Dict[str, str]
        A dictionary of guardrail names and their configurations. Choose from:
        continuation, dan, encoding, goodside, knownbadsignatures, leakreplay,
        lmrc, malwaregen, packagehallucination, realpublicityprompts, snowball, xss.
    """
    pass

def get_vulnerability_guardrails():
    """
    Get the currently enabled vulnerability guardrails.
    
    Returns
    -------
    guardrails : List[str]
        List of currently enabled vulnerability guardrails.
    """
    pass

def set_input_guardrail(guardrail: str, config: Any):
    """
    Set an input guardrail.
    
    Supported guardrails: jailbreak detection, sanitization, input moderation.

    Parameters
    ----------
    guardrail : str
        The name of the input guardrail to set.
    config : Any
        The configuration details for the input guardrail.
    """
    pass

def get_input_guardrails():
    """
    Get all enabled input guardrails.
    
    Returns
    -------
    input_guardrails : List[str]
        List of all enabled input guardrails.
    """
    pass

def set_dialog_guardrail(guardrail: str, config: Any):
    """
    Set a dialog guardrail.
    
    Parameters
    ----------
    guardrail : str
        The name of the dialog guardrail to set.
    config : Any
        The configuration details for the dialog guardrail.
    """
    pass

def get_dialog_guardrails():
    """
    Get all enabled dialog guardrails.
    
    Returns
    -------
    dialog_guardrails : List[str]
        List of all enabled dialog guardrails.
    """
    pass

def set_retrieval_guardrail(guardrail: str, config: Any):
    """
    Set a retrieval guardrail.

    Supported guardrails: sanitization, data access.

    Parameters
    ----------
    guardrail : str
        The name of the retrieval guardrail to set.
    config : Any
        The configuration details for the retrieval guardrail.
    """
    pass

def get_retrieval_guardrails():
    """
    Get all enabled retrieval guardrails.
    
    Returns
    -------
    retrieval_guardrails : List[str]
        List of all enabled retrieval guardrails.
    """
    pass

def set_execution_guardrail(guardrail: str, config: Any):
    """
    Set an execution guardrail.

    Supported guardrails: access.

    Parameters
    ----------
    guardrail : str
        The name of the execution guardrail to set.
    config : Any
        The configuration details for the execution guardrail.
    """
    pass

def get_execution_guardrails():
    """
    Get all enabled execution guardrails.
    
    Returns
    -------
    execution_guardrails : List[str]
        List of all enabled execution guardrails.
    """
    pass

def set_output_guardrail(guardrail: str, config: Any):
    """
    Set an output guardrail.

    Supported guardrails: sanitization, fact checking, hallucination,
    moderation.

    Parameters
    ----------
    guardrail : str
        The name of the output guardrail to set.
    config : Any
        The configuration details for the output guardrail.
    """
    pass

def get_output_guardrails():
    """
    Get all enabled output guardrails.
    
    Returns
    -------
    output_guardrails : List[str]
        List of all enabled output guardrails.
    """
    pass
