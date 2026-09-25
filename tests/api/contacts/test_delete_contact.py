from conftest import ContactInfo
from handlers.api.contacts import DeleteContact
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestDeleteContact:
    def test_delete_contact_success(self, class_contact: ContactInfo):
        endpoint = DeleteContact(
            {"contact_id": class_contact.id},
            {},
            INTERCOM_ACCESS_TOKEN,
        )

        response = endpoint.execute()
        assert response.get("status") != "error", response
        assert response.get("deleted") is True
        assert response.get("id") == class_contact.id
        assert response.get("external_id") == class_contact.external_id

    def test_delete_contact_invalid_token_returns_401(self):
        endpoint = DeleteContact(
            {"contact_id": "invalid_contact_id"},
            {},
            "invalid_token",
        )

        response = endpoint.execute()

        assert response["status"] == "error"
        assert response["code"] == 401
