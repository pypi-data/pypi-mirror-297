import json
import logging
import os

import requests

__version__ = "0.1.0"

URL = "https://api.alwaysdata.com/v1/{what}/"
# get API credentials environment variables
apikey = os.getenv("AD_APIKEY")
account = os.getenv("AD_ACCOUNT")
CREDENTIALS = (f"{apikey} account={account}", "")

EMPTY_TOKENS_CONFIG = {
    "_changeme_": {
        "domain": "domain.extension",
        "account": "user@domain.extension",
        "token": "Alwaysdata API Token",
        "redirect": "user@domain.extension",
    }
}


def forge_url(what):
    """forge appropriate URL for AD domains

    >>> forge_url("toto")
    'https://api.alwaysdata.com/v1/toto/'
    """
    what = what.strip("/").lstrip("v1/")
    url = URL.format(what=what)
    return url


def requests_get(what_to_search):
    """forge an url from URL global var and sends a request to this url.
    If returned code is OK, return decoded server response as a python object.

    >>> requests_get("account")
    [{'id': ...}]
    """
    url = forge_url(what=what_to_search)
    # Send HTTP request
    response = requests.get(
        url,
        auth=CREDENTIALS,
    )
    if response.ok is False:
        msg = f"{url}:: code{response.status_code}"
        logging.error(msg)
        raise ValueError(msg)
    return json.loads(response.content.decode())
