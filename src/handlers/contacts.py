from handlers.utils.body_builder import build_body
from handlers.utils.constants import INTERCOM_API_BASE_URL, SHARED_HEADERS
from handlers.utils.make_request import make_request
from handlers.utils.url_builder import build_url


class BaseContacts:
    base_path = f"{INTERCOM_API_BASE_URL}/contacts"

    def __init__(self, inputs: dict, context: dict):
        self.inputs = inputs
        self.context = context
        self.token = context.get("env", {}).get("INTERCOM_ACCESS_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
        }
        self.headers.update(SHARED_HEADERS)

    def _make_request(self, url: str, method="GET", body: dict | None = None) -> dict:
        return make_request(url, method, body, self.headers)


class ListContacts(BaseContacts):
    def __init__(self, inputs: dict, context: dict) -> None:
        super().__init__(inputs, context)
        self.url = build_url(self.base_path, ["per_page", "starting_after"], inputs)

    def execute(self) -> dict:
        return self._make_request(self.url)


class CreateContact(BaseContacts):
    def __init__(self, inputs: dict, context: dict) -> None:
        super().__init__(inputs, context)
        self.url = build_url(self.base_path, [], inputs)
        self.body = build_body(["email"], inputs)

    def execute(self):
        return self._make_request(self.url, "POST", self.body)
