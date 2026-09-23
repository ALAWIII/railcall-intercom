from typing import Any

NOISE_MARKERS = frozenset(
    {
        None,
        "",
        "N/A",
        "n/a",
        "None",
        "null",
        "undefined",
        "unknown",
        "TBD",
        "pending",
        "not_set",
        "not_provided",
        "not_available",
        "1970-01-01T00:00:00Z",
        "0001-01-01T00:00:00Z",
    }
)

NOISE_KEYS = frozenset({"type", "has_more", "url", "_links"})


def _is_noise(value):
    """Check if a value is noise. Preserves False and 0."""
    # Handle unhashable types (lists, dicts) first
    if isinstance(value, (list, dict)):
        return len(value) == 0

    # Only hashable values reach here
    return value in NOISE_MARKERS


def clean_response(data) -> dict[Any, Any] | list[Any] | Any:
    """Recursively remove noise from nested dicts and lists."""
    if isinstance(data, dict):
        return {
            key: result
            for key, value in data.items()
            if key not in NOISE_KEYS and not _is_noise(result := clean_response(value))
        }

    if isinstance(data, list):
        return [
            result for item in data if not _is_noise(result := clean_response(item))
        ]

    return data
