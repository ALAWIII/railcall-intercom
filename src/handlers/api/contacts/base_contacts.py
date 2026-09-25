from handlers.utils import INTERCOM_API_BASE_URL, SHARED_HEADERS, make_request

CONTACT_FIELDS = [
    "email",
    "role",
    "external_id",
    "phone",
    "email_verified",
    "name",
    "avatar",
    "signed_up_at",
    "last_seen_at",
    "owner_id",
    "unsubscribed_from_emails",
    "custom_attributes",
]


class BaseContacts:
    base_path = f"{INTERCOM_API_BASE_URL}/contacts"

    def __init__(self, inputs: dict, context: dict, token: str):
        self.inputs = inputs
        self.context = context
        self.headers = {
            "Authorization": f"Bearer {token}",
        }
        self.headers.update(SHARED_HEADERS)

    def _make_request(self, url: str, method="GET", body: dict | None = None) -> dict:
        return make_request(url, method, body, self.headers)
