from handlers.api import ListContacts
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestListContacts:
    """Test ListContacts endpoint logic."""

    def test_list_contacts_returns_200(self):
        lc = ListContacts({"per_page": 5}, {}, INTERCOM_ACCESS_TOKEN)
        response = lc.execute()

        # 1. Not an error response
        assert "status" not in response or response.get("status") != "error"

        # 2. Expected keys exist
        assert "data" in response
        assert "total_count" in response

        # 3. Correct types
        assert isinstance(response["data"], list)
        assert isinstance(response["total_count"], int)

        # 4. Respects per_page limit
        assert len(response["data"]) <= 5

        # 5. Each contact has core fields and no noise
        for contact in response["data"]:
            assert "id" in contact
            assert "type" not in contact  # stripped by NOISE_KEYS
            assert "phone" not in contact or contact["phone"] is not None
            assert "avatar" not in contact or contact["avatar"] is not None

        # 6. Timestamps are converted to ISO strings
        for contact in response["data"]:
            if "created_at" in contact:
                assert isinstance(contact["created_at"], str)
                assert "T" in contact["created_at"]

    def test_list_contacts_invalid_token_returns_error(self):
        bad_access_token = "invalid_token"
        lc = ListContacts({}, {}, bad_access_token)
        response = lc.execute()

        assert response["status"] == "error"
        assert response["code"] == 401
