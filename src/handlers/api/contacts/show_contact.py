from handlers.api.contacts.base_contacts import BaseContacts
from handlers.utils import build_url
from handlers.utils.input_validator import InputValidator

query_parameters = ["include_merge_history"]
path_parameters = ["contact_id"]

exactly = [{"fields": path_parameters, "count": 1}]


class ShowContact(BaseContacts):
    def __init__(self, inputs: dict, context: dict, access_token: str) -> None:
        InputValidator(inputs, exactly=exactly).validate()
        super().__init__(inputs, context, access_token)
        self.contact_id: str = inputs[path_parameters[0]]
        self.url = build_url(
            f"{self.base_path}/{self.contact_id}", query_parameters, inputs
        )

    def execute(self) -> dict:
        return self._make_request(self.url)
