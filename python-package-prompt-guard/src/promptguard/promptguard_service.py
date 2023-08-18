"""
This module exposes wrappers around API calls to the PromptGuard service.
"""
import json
from dataclasses import dataclass
from http import HTTPStatus
from http.client import HTTPException
from typing import Dict, List, Union

from atls import AttestedHTTPSConnection, AttestedTLSContext
from atls.validators import AZ_AAS_GLOBAL_JKUS, AzAasAciValidator, Validator
from promptguard.authentication import get_api_key
from promptguard.configuration import get_server_config


@dataclass
class SanitizeResponse:
    sanitized_text: str
    secure_context: bytes


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
    response = _send_request_to_promptguard_service(
        endpoint="/sanitize", payload={"text": text}
    )
    return SanitizeResponse(**json.loads(response))


@dataclass
class DesanitizeResponse:
    desanitized_text: str


def desanitize(
    sanitized_text: str, secure_context: bytes
) -> DesanitizeResponse:
    """
    Takes in a sanitized response and returns the desanitized
    text with PII added back to it.

    Parameters
    ----------
    sanitized_text : str
        Sanitized response that you want to be desanitized.
    secure_context : bytes
        Secret entropy value that should have been returned by
        the call to `sanitize`.

    Returns
    -------
    DesanitizeResponse
        The deanonymzied version of `sanitized_text` with PII added back in.
    """
    response = _send_request_to_promptguard_service(
        endpoint="/desanitize",
        payload={
            "sanitized_text": sanitized_text,
            "secure_context": secure_context,
        },
    )
    return DesanitizeResponse(**json.loads(response))


########## Helper Functions ##########


def _send_request_to_promptguard_service(
    endpoint: str, payload: Dict[str, Union[str, bytes]]
) -> str:
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
    str
        The response body returned by the request, only returned
        if the request was successful
    """

    api_key = get_api_key()
    hostname, port = get_server_config()

    ctx = AttestedTLSContext(_get_default_validators())
    conn = AttestedHTTPSConnection(hostname, ctx, port)

    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        conn.request(
            "POST",
            endpoint,
            json.dumps(payload),
            headers,
        )

        response = conn.getresponse()

        response_code = response.getcode()
        response_body = response.read()
        response_text = response_body.decode()

        if response_code != HTTPStatus.OK:
            raise HTTPException(
                f"Error response from the PromptGuard server: "
                f"[HTTP {response_code}] {response_text}"
            )

        return response_text
    finally:
        conn.close()


def _get_default_validators() -> List[Validator]:
    """
    Retrieve a list of default aTLS validators to use when connecting to the
    PromptGuard server with sane default configurations.

    Returns
    -------
    list of Validator
        One or more aTLS validators
    """
    az_aas_aci_validator = AzAasAciValidator(jkus=AZ_AAS_GLOBAL_JKUS)

    return [az_aas_aci_validator]
