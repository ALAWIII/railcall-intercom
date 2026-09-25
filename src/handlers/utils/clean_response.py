from datetime import datetime, timezone
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

NOISE_KEYS = frozenset({"has_more", "url", "_links"})

# Add a separate set for noise type values
NOISE_TYPE_VALUES = frozenset(
    {"pages", "addressable_list", "error.list", "location", "list", "array", "string"}
)


def _is_noise(value):
    """Check if a value is noise. Preserves False and 0."""
    # Handle unhashable types (lists, dicts) first
    if isinstance(value, (list, dict)):
        return len(value) == 0

    # Only hashable values reach here
    return value in NOISE_MARKERS


def _format_timestamp(value):
    """Converts Unix timestamp (seconds) to readable ISO-8601 string."""
    try:
        # Intercom uses seconds, not milliseconds
        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
    except (ValueError, TypeError, OSError):
        return value


def clean_response(data) -> dict[Any, Any] | list[Any] | Any:
    """Recursively remove noise from nested dicts and lists."""
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            if key in NOISE_KEYS:
                continue

            # Strip "type" only if it's a structural wrapper, not a domain value
            if key == "type" and value in NOISE_TYPE_VALUES:
                continue

            # Format Unix timestamps to ISO-8601
            if key.endswith("_at") and isinstance(value, (int, float)) and value > 0:
                result = _format_timestamp(value)
            else:
                result = clean_response(value)

            if not _is_noise(result):
                cleaned[key] = result
        return cleaned

    if isinstance(data, list):
        return [
            result for item in data if not _is_noise(result := clean_response(item))
        ]

    return data
