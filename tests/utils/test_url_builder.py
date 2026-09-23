from urllib.parse import parse_qs, urlparse

from handlers.utils.constants import INTERCOM_API_BASE_URL
from handlers.utils.url_builder import build_url


def test_build_url_full_params():
    url = build_url(
        f"{INTERCOM_API_BASE_URL}",
        ["starting_after", "per_page"],
        {"starting_after": "hello", "per_page": 55},
    )
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    assert params["starting_after"] == ["hello"]
    assert params["per_page"] == ["55"]


def test_build_url_partial_params():
    url = build_url(
        f"{INTERCOM_API_BASE_URL}",
        ["starting_after", "per_page"],
        {"starting_after": "hello"},
    )
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    assert params["starting_after"] == ["hello"]


def test_build_url_no_params():
    url = build_url(
        f"{INTERCOM_API_BASE_URL}",
        ["starting_after", "per_page"],
        {},
    )
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    assert params.get("starting_after") == None
    assert params.get("per_page") == None
