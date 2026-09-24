from handlers.api.contacts.base_contacts import BaseContacts
from handlers.utils import build_url


class ListContacts(BaseContacts):
    def __init__(self, inputs: dict, context: dict, access_token: str) -> None:
        super().__init__(inputs, context, access_token)
        self.url = build_url(self.base_path, ["per_page", "starting_after"], inputs)

    def execute(self) -> dict:
        return self._make_request(self.url)
