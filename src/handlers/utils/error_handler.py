import json
import urllib.error


def handle_api_error(e: Exception) -> dict:
    """Reusable error handler for all Intercom endpoints."""

    if isinstance(e, urllib.error.HTTPError):
        try:
            error_body = e.read().decode("utf-8")
            error_data = json.loads(error_body)
            message = error_data.get("errors", [{}])[0].get("message", error_body)
        except (json.JSONDecodeError, IndexError, KeyError):
            message = error_body

        return {"status": "error", "code": e.code, "message": message}

    elif isinstance(e, urllib.error.URLError):
        return {"status": "error", "message": f"Network error: {e.reason}"}

    elif isinstance(e, json.JSONDecodeError):
        return {"status": "error", "message": f"Invalid JSON response: {e}"}

    elif isinstance(e, TimeoutError):
        return {"status": "error", "message": "Request timed out"}

    else:
        return {"status": "error", "message": f"Unexpected error: {e!s}"}
