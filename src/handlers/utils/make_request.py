import json
import urllib
import urllib.request
from typing import cast

from handlers.utils.clean_response import clean_response
from handlers.utils.error_handler import handle_api_error


def make_request(
    url: str, method: str = "GET", body: dict | None = None, headers: dict | None = None
) -> dict:
    """Reusable HTTP request with error handling for all endpoints."""
    headers = {} if headers is None else headers
    try:
        data = json.dumps(body).encode("utf-8") if body else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        return cast(dict, clean_response(result))

    except Exception as e:
        return handle_api_error(e)
