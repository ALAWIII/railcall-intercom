from handlers.api.contacts.base_contacts import BaseContacts


class ShowContact(BaseContacts):
    def __init__(self, inputs: dict, context: dict) -> None:
        """here will extract the required fields to satisfy ShowContact operation from input and context."""

    def execute(self):
        pass

    def test_create_contact_invalid_token_returns_error(self):
        pass
