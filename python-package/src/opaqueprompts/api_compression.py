from typing import List

def enable_compression(rate: float, force_tokens: List[str]):
    """
    Turn on prompt compression. This operation is idempotent.
    
    Parameters
    ----------
    rate : float
        Compression rate.
    force_tokens : List[str]
        List of tokens to keep post-compression.
    """
    pass

def disable_compression():
    """
    Turn off prompt compression. This operation is idempotent.
    """
    pass