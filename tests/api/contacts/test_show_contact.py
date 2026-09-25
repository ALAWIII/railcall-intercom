import uuid

import pytest

from handlers.api.contacts import CreateContact, ShowContact
from tests.support.constants import INTERCOM_ACCESS_TOKEN


@pytest.fixture(scope="class")
def contact_id():
    if not INTERCOM_ACCESS_TOKEN:
        pytest.skip("Missing INTERCOM_ACCESS_TOKEN")

    unique = uuid.uuid4().hex

    inputs = {
        "email": f"railcall-{unique}@example.com",
        "external_id": f"railcall-{unique}",
    }

    response = CreateContact(inputs, {}, INTERCOM_ACCESS_TOKEN).execute()

    assert response.get("status") != "error", response
    assert response.get("id"), response

    return response["id"]


class TestShowContact:
    def test_show_contact_success(self, contact_id):
        endpoint = ShowContact({"contact_id": contact_id}, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()

        assert response.get("status") != "error", response
        assert response.get("id") == contact_id

    def test_show_contact_invalid_token_returns_401(self, contact_id):
        endpoint = ShowContact({"contact_id": contact_id}, {}, "invalid_token")
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
