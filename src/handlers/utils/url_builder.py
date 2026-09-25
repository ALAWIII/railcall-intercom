from urllib.parse import urlencode


def build_url(base_url: str, params: list[str], inputs: dict) -> str:
    """Build URL by extracting specified query params from inputs.

    Extract only the requested params, skipping missing or None values
    """
    filtered = {k: inputs[k] for k in params if inputs.get(k) is not None}

    if not filtered:
        return base_url

    return f"{base_url}?{urlencode(filtered)}"
