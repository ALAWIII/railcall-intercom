from handlers.api.contacts import ShowContact
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestShowContact:
    def test_show_contact_success(self, class_contact_id):
        endpoint = ShowContact(
            {"contact_id": class_contact_id}, {}, INTERCOM_ACCESS_TOKEN
        )
        response = endpoint.execute()

        assert response.get("status") != "error", response
        assert response.get("id") == class_contact_id

    def test_show_contact_invalid_token_returns_401(self, class_contact_id):
        endpoint = ShowContact({"contact_id": class_contact_id}, {}, "invalid_token")
        response = endpoint.execute()

        assert response["status"] == "error"
        assert response["code"] == 401

    # @pytest.mark.skipif(
    #     not MERGED_CONTACT_ID,
    #     reason="Set INTERCOM_MERGED_CONTACT_ID to a merged-away contact ID",
    # )
    # def test_show_merged_contact_returns_410(self):
    #     endpoint = ShowContact({"contact_id": MERGED_CONTACT_ID}, CONTEXT, TOKEN)
    #     response = endpoint.execute()

    #     assert response["status"] == "error"
    #     assert response["code"] == 410
