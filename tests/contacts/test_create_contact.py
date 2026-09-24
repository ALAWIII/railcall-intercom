import uuid

from handlers.api import CreateContact
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestCreateContact:
    def test_create_contact_returns_200(self):
        # Generate unique email for each test run
        unique_email = f"test-{uuid.uuid4()}@example.com"

        cc = CreateContact({"email": unique_email}, {}, INTERCOM_ACCESS_TOKEN)
        response = cc.execute()
        # Assert success
        assert "status" not in response or response.get("status") != "error"

        assert "id" in response
        # "Assert contact was created"
        assert response["email"] == unique_email

    def test_create_contact_invalid_token_returns_error(self):
        bad_access_token = "invalid_token"
        expected_response = {
            "code": 401,
            "message": "Access Token Invalid",
            "status": "error",
        }
        cc = CreateContact({"email": "shawarma@hotgirl.com"}, {}, bad_access_token)
        response = cc.execute()

        assert response == expected_response
