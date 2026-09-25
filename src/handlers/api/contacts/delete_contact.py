from handlers.api.contacts.base_contacts import BaseContacts
from handlers.utils import InputValidator

path_parameters = ["contact_id"]
exactly = [{"fields": path_parameters, "count": 1}]


class DeleteContact(BaseContacts):
    def __init__(self, inputs: dict, context: dict, access_token: str):
        InputValidator(inputs, exactly=exactly).validate()
        super().__init__(inputs, context, access_token)
        self.contact_id = inputs[path_parameters[0]]
        self.url = f"{self.base_path}/{self.contact_id}"

    def execute(self):
        return self._make_request(self.url, "DELETE")
