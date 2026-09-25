import uuid

from handlers.api.contacts import UpdateContact
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestUpdateContact:
    def test_update_contact_success(self, class_contact):
        new_name = f"Railcall Updated {uuid.uuid4().hex[:8]}"

        endpoint = UpdateContact(
            {
                "contact_id": class_contact.id,
                "name": new_name,
            },
            {},
            INTERCOM_ACCESS_TOKEN,
        )

        response = endpoint.execute()

        assert response.get("status") != "error", response
        assert response.get("id") == class_contact.id
        assert response.get("name") == new_name

    def test_update_contact_invalid_token_returns_401(self):
        endpoint = UpdateContact(
            {
                "contact_id": "not-important",
                "name": "Should Not Update",
            },
            {},
            "invalid_token",
        )

        response = endpoint.execute()

        assert response["status"] == "error"
        assert response["code"] == 401
