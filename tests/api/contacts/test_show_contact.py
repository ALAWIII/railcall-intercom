from conftest import ContactInfo
from handlers.api.contacts import ShowContact
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestShowContact:
    def test_show_contact_success(self, class_contact: ContactInfo):
        endpoint = ShowContact(
            {"contact_id": class_contact.id}, {}, INTERCOM_ACCESS_TOKEN
        )
        response = endpoint.execute()

        assert response.get("status") != "error", response
        assert response.get("id") == class_contact.id

    def test_show_contact_invalid_token_returns_401(self, class_contact: ContactInfo):
        endpoint = ShowContact({"contact_id": class_contact.id}, {}, "invalid_token")
        response = endpoint.execute()

        assert response["status"] == "error"
        assert response["code"] == 401
