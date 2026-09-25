from handlers.api.contacts.base_contacts import BaseContacts
from handlers.utils import InputValidator, build_body, build_url

query_parameters = ["include_merge_history"]
body_fields = ["from", "into", "skip_duplicate_validation"]

exactly = [{"fields": body_fields[0:2], "count": 2}]


class MergeContact(BaseContacts):
    def __init__(self, inputs: dict, context: dict, access_token: str):
        InputValidator(inputs, exactly=exactly).validate()
        super().__init__(inputs, context, access_token)
        self.url = build_url(f"{self.base_path}/merge", query_parameters, inputs)
        self.body = build_body(body_fields, inputs)

    def execute(self):
        return self._make_request(self.url, "POST", self.body)
