def build_body(keys: list[str], inputs: dict) -> dict:
    """Build request body by extracting specified keys from inputs."""
    return {k: inputs[k] for k in keys if inputs.get(k) is not None}
