"""
This module handles configuration logic for the opaqueprompts package.
"""

import os
from typing import Tuple

# TODO: Once we have deployed the OpaquePrompts Service this should be
# hardcoded to use that domain, as end users shouldn't need to configure
# the domain name manually.
SERVER_HOSTNAME_ENV_VAR = "OPAQUEPROMPTS_SERVER_HOSTNAME"
SERVER_PORT_ENV_VAR = "OPAQUEPROMPTS_SERVER_PORT"

DEFAULT_SERVER_PORT = 443


def get_server_config() -> Tuple[str, int]:
    """
    Retrieve from the environment the hostname or IP address and the port
    number of the OpaquePrompts service to use. If the corresponding
    environment variables are not set, defaults will be returned.

    Returns
    -------
    (str, int)
        The hostname or IP and the port number to use
    """
    hostname = os.environ.get(
        SERVER_HOSTNAME_ENV_VAR, "api.opaqueprompts.opaque.co"
    )
    if not hostname:
        raise Exception(
            f"Unable to read the OpaquePrompts server hostname, \
            ensure the {SERVER_HOSTNAME_ENV_VAR} environment variable is set."
        )

    port_str = os.environ.get(SERVER_PORT_ENV_VAR, "443")
    if port_str is not None:
        port = int(port_str)
    else:
        port = DEFAULT_SERVER_PORT

    return (hostname, port)
