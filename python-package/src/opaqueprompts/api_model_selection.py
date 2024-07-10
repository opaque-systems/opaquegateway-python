from typing import Dict
from typing import Any

def configure_model_selection(config: Dict[str, str], default: str):
    """
    Configure when to use what model.

    When called, intelligent model selection is enabled.
    
    Parameters
    ----------
    config : Dict[str, str]
        A dictionary of model names to a natural language description of when
        to use each model.
    default : str
        The name of the default model to use.
    """
    pass
