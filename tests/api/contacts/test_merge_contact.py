import uuid

from handlers.api.contacts import CreateContact, MergeContact, ShowContact
from tests.support.constants import INTERCOM_ACCESS_TOKEN


def _create_contact(role: str) -> dict:
    unique = uuid.uuid4().hex

    inputs = {
        "email": f"railcall-merge-{unique}@example.com",
        "external_id": f"railcall-merge-{unique}",
        "role": role,
    }

    response = CreateContact(inputs, {}, INTERCOM_ACCESS_TOKEN).execute()

    assert response.get("status") != "error", response
    assert response.get("id"), response

    return response


class TestMergeContact:
    def test_merge_contact_success(self):
        lead = _create_contact("lead")
        user = _create_contact("user")

        endpoint = MergeContact(
            {
                "from": lead["id"],
                "into": user["id"],
                "skip_duplicate_validation": True,
            },
            {},
            INTERCOM_ACCESS_TOKEN,
        )

        response = endpoint.execute()

        assert response.get("status") != "error", response
        assert response.get("id") == user["id"]
        assert response.get("role") == "user"
        # ============== check 410 Gone after success merging the contact
        show_endpoint = ShowContact(
            {"contact_id": lead["id"]},
            {},
            INTERCOM_ACCESS_TOKEN,
        )

        show_response = show_endpoint.execute()

        assert show_response["status"] == "error"
        assert show_response["code"] == 410
        assert "merged" in show_response["message"].lower()

    def test_merge_contact_bad_request(self):
        user_one = _create_contact("user")
        user_two = _create_contact("user")

        endpoint = MergeContact(
            {
                "from": user_one["id"],
                "into": user_two["id"],
                "skip_duplicate_validation": True,
            },
            {},
            INTERCOM_ACCESS_TOKEN,
        )

        response = endpoint.execute()

        assert response["status"] == "error"
        assert response["code"] == 400

    def test_merge_contact_invalid_token_returns_401(self):
        endpoint = MergeContact(
            {
                "from": "000000000000000000000000",
                "into": "000000000000000000000000",
                "skip_duplicate_validation": True,
            },
            {},
            "invalid_token",
        )

        response = endpoint.execute()

        assert response["status"] == "error"
        assert response["code"] == 401
