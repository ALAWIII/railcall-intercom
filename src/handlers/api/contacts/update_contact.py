from handlers.api.contacts.base_contacts import CONTACT_FIELDS, BaseContacts
from handlers.utils import InputValidator, build_body, build_url

path_parameters = ["contact_id"]
query_parameters = ["include_merge_history"]

exactly = [{"fields": path_parameters, "count": 1}]
at_least = [{"fields": CONTACT_FIELDS, "count": 1}]


class UpdateContact(BaseContacts):
    def __init__(self, inputs: dict, context: dict, access_token: str):
        InputValidator(inputs, exactly=exactly, at_least=at_least).validate()
        super().__init__(inputs, context, access_token)
        self.contact_id = inputs[path_parameters[0]]
        self.url = build_url(
            f"{self.base_path}/{self.contact_id}", query_parameters, inputs
        )
        self.body = build_body(CONTACT_FIELDS, inputs)

    def execute(self):
        return self._make_request(self.url, "PUT", self.body)
