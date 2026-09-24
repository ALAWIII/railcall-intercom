from handlers.api.contacts.base_contacts import BaseContacts
from handlers.utils import InputValidator, build_body, build_url

create_contact_body_fields = [
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
at_least = [{"fields": ["email", "role", "external_id"], "count": 1}]


class CreateContact(BaseContacts):
    def __init__(self, inputs: dict, context: dict, access_token: str) -> None:
        InputValidator(inputs, at_least=at_least).validate()
        super().__init__(inputs, context, access_token)
        self.url = build_url(self.base_path, [], inputs)

        self.body = build_body(
            create_contact_body_fields,
            inputs,
        )

    def execute(self):
        return self._make_request(self.url, "POST", self.body)
