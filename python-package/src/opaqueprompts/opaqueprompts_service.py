"""
This module exposes wrappers around API calls to the OpaquePrompts service.
"""
import json
import os
import threading
from dataclasses import dataclass
from http import HTTPStatus
from http.client import HTTPException
from importlib import metadata
from typing import Dict, List, Optional, Union

import requests
from atls.utils.requests import HTTPAAdapter
from atls.validators import Validator
from atls.validators.azure.aas import PUBLIC_JKUS, AciValidator
from opaqueprompts.authentication import get_api_key
from opaqueprompts.configuration import get_server_config

# Global requests session to leverage connection pooling to in turn avoid
# establishing a new connection for each request to the service.
_session: Optional[requests.Session] = None

# Protects the global requests session when creating it for the first time.
_session_lock: threading.Lock = threading.Lock()


@dataclass
class SanitizeResponse:
    """
    Class representing the return value of the sanitize method

    Attributes
    ----------
    sanitized_texts : list of str
        The sanitized form of the input texts without PII. List has the same
        dimensions as the input_texts list.
    secret_entropy : str
        A set of bytes encoded as a string that contains the context needed to
        desanitize the entities in sanitized_text; it must be passed along to
        the desanitize endpoint.
    """

    sanitized_texts: List[str]
    secure_context: str


def sanitize(
    input_texts: List[str],
    retries: Optional[int] = None,
    timeout: Optional[int] = None,
) -> SanitizeResponse:
    """
    Takes in a list of prompts and returns a list of sanitized prompts with PII
    redacted from it.

    Parameters
    ----------
    input_texts : list of str
        List of prompts to sanitize together.
    retries : int, optional
        The number of retries to submit a request to the service before giving
        up when errors occur.
    timeout : int, optional
        The number of seconds to wait until a request to the service times out.

    Returns
    -------
    SanitizeResponse
        The anonymized version of input_texts without PII and a secret entropy
        value.
    """
    response = _send_request_to_opaqueprompts_service(
        endpoint="sanitize",
        payload={"input_texts": input_texts},
        retries=retries,
        timeout=timeout,
    )
    return SanitizeResponse(**json.loads(response))


@dataclass
class DesanitizeResponse:
    """
    Class representing the return value of the desanitize method.

    Attributes
    ----------
    desanitized_text : str
        The desanitized form of the input text with PII added back in.
    """

    desanitized_text: str


def desanitize(
    sanitized_text: str,
    secure_context: str,
    retries: Optional[int] = None,
    timeout: Optional[int] = None,
) -> DesanitizeResponse:
    """
    Takes in a sanitized response and returns the desanitized text with PII
    added back to it.

    Parameters
    ----------
    sanitized_text : str
        Sanitized response that you want to be desanitized.
    secure_context : str
        Secret entropy value that should have been returned by the call to
        sanitize.
    retries : int, optional
        The number of times to resubmit a request to the service before giving
        up when errors occur.
    timeout : int, optional
        The number of seconds to wait until a request to the service times out.

    Returns
    -------
    DesanitizeResponse
        The deanonymzied version of sanitized_text with PII added back in.
    """
    response = _send_request_to_opaqueprompts_service(
        endpoint="desanitize",
        payload={
            "sanitized_text": sanitized_text,
            "secure_context": secure_context,
        },
        retries=retries,
        timeout=timeout,
    )
    return DesanitizeResponse(**json.loads(response))


########## Helper Functions ##########


def _send_request_to_opaqueprompts_service(
    endpoint: str,
    payload: Dict[str, Union[str, List[str]]],
    retries: Optional[int] = None,
    timeout: Optional[int] = None,
) -> str:
    """
    Helper method which takes in the name of the endpoint and a payload
    dictionary, and converts it into the form needed to send the request to the
    OpaquePrompts service. Returns the response received if it's successful,
    and raises an error otherwise.

    Parameters
    ----------
    endpoint : str
        The name of the endpoint you are trying to hit.
    payload : dict
        The payload of the request as a dictionary.
    retries : int, optional
        The number of times to resubmit a request to the service before giving
        up when errors occur.
    timeout : int, optional
        The number of seconds to wait until a request to the service times out.

    Returns
    -------
    str
        The response body returned by the request, only returned if the request
        was successful.
    """

    global _session
    global _session_lock

    # This flag is used to disable aTLS for testing purposes.
    # INTERNAL USE ONLY.
    # It breaks the communication with the aTLS enabled server.
    _client_atls_enabled = bool(
        os.environ.get("OPAQUEPROMPTS_CLIENT_ATLS_ENABLED", True)
    )
    http_protocol = "httpa" if _client_atls_enabled else "http"

    with _session_lock:
        if _session is None:
            _session = requests.Session()
            if _client_atls_enabled:
                _session.mount(
                    "httpa://", HTTPAAdapter(_get_default_validators())
                )

    api_key = get_api_key()
    hostname, port = get_server_config()

    if retries is None:
        retries = 3

    conn_except: ConnectionError
    while retries > 0:
        try:
            response = _session.request(
                "POST",
                f"{http_protocol}://{hostname}:{port}/{endpoint}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Client-Version": metadata.version("opaqueprompts"),
                },
                data=json.dumps(payload),
                timeout=timeout,
            )

            response_code = response.status_code
            response_text = response.text

            if response_code != HTTPStatus.OK:
                raise HTTPException(
                    f"Error response from the OpaquePrompts server: "
                    f"[HTTP {response_code}] {response_text}"
                )

            return response_text
        except ConnectionError as e:
            conn_except = e
            retries -= 1

    raise conn_except


def _get_default_validators() -> List[Validator]:
    """
    Retrieve a list of default aTLS validators to use when connecting to the
    OpaquePrompts server with sane default configurations.

    Returns
    -------
    list of Validator
        One or more aTLS validators
    """
    aci_validator = AciValidator(jkus=PUBLIC_JKUS)

    return [aci_validator]
