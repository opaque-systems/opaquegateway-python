"""
This module exposes wrappers around API calls to the Promptguard service.
"""
import json
import os
from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, Union

import requests
from promptguard.authentication import get_access_token

# TODO: Once we have deployed the Promptguard Service this should be hardcoded
# to use that domain, as end users shouldn't need to configure the
# domain name manually.
PROMPTGUARD_SERVICE_DOMAIN_NAME = os.environ.get(
    "PROMPTGUARD_SERVICE_DOMAIN_NAME"
)


@dataclass
class SanitizeResponse:
    sanitized_text: str
    secret_entropy: bytes


def sanitize(text: str) -> SanitizeResponse:
    """
    Takes in a text prompt and returns the sanitized
    text with PII redacted from it.

    Parameters
    ----------
    text : str
        Prompt that you want to be sanitized.

    Returns
    -------
    SanitizeResponse
        The anonymzied version of text without PII and
        a secret entropy value.
    """
    response = _send_request_to_ppp_service(
        endpoint="sanitize", payload={"text": text}
    )
    return SanitizeResponse(**json.loads(response.text))


@dataclass
class DesanitizeResponse:
    desanitized_text: str


def desanitize(
    sanitized_text: str, secret_entropy: bytes
) -> DesanitizeResponse:
    """
    Takes in a sanitized response and returns the desanitized
    text with PII added back to it.

    Parameters
    ----------
    sanitized_text : str
        Sanitized response that you want to be desanitized.
    secret_entropy : bytes
        Secret entropy value that should have been returned by
        the call to `sanitize`.

    Returns
    -------
    DesanitizeResponse
        The deanonymzied version of `sanitized_text` with PII added back in.
    """
    response = _send_request_to_ppp_service(
        endpoint="desanitize",
        payload={
            "sanitized_text": sanitized_text,
            "secret_entropy": secret_entropy,
        },
    )
    return DesanitizeResponse(**json.loads(response.text))


########## Helper Functions ##########


def _send_request_to_ppp_service(
    endpoint: str, payload: Dict[str, Union[str, bytes]]
) -> requests.Response:
    """
    Helper method which takes in the name of the endpoint, and a
    payload dictionary, and converts it into the form needed to send
    the request to the Promptguard service. Returns the response
    recieved if its successful, and raises an error otherwise.

    Parameters
    ----------
    endpoint : str
        The name of the endpoint you are trying to hit
    payload : dict
        The payload of the request as a dictionary

    Returns
    -------
    requests.Response
        The response object returned by the request, only returned
        if the request was successful
    """
    endpoint_url = f"http://{PROMPTGUARD_SERVICE_DOMAIN_NAME}/{endpoint}"
    access_token = get_access_token()
    response = requests.request(
        "POST",
        endpoint_url,
        headers={"Authorization": f"Bearer {access_token}"},
        data=json.dumps(payload),
    )
    if response.status_code != HTTPStatus.OK:
        raise Exception(
            f"Error response from {endpoint_url}: "
            f"[HTTP {response.status_code}] {response.text}"
        )
    return response
