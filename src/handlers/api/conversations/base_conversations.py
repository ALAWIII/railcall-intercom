from handlers.utils import INTERCOM_API_BASE_URL, SHARED_HEADERS, make_request


class BaseConversations:
    base_path = f"{INTERCOM_API_BASE_URL}/conversations"

    def __init__(self, inputs: dict, context: dict, token: str):
        self.inputs = inputs
        self.context = context
        self.headers = {
            "Authorization": f"Bearer {token}",
        }
        self.headers.update(SHARED_HEADERS)

    def _make_request(self, url: str, method="GET", body: dict | None = None) -> dict:
        return make_request(url, method, body, self.headers)
