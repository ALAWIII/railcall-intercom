import uuid

from handlers.contacts import CreateContact
from tests.support.constants import CONTEXT


class TestCreateContact:
    def test_create_contact_returns_200(self):
        # Generate unique email for each test run
        unique_email = f"test-{uuid.uuid4()}@example.com"

        cc = CreateContact({"email": unique_email}, CONTEXT)
        response = cc.execute()
        # Assert success
        assert "status" not in response or response.get("status") != "error"

        assert "id" in response
        # "Assert contact was created"
        assert response["email"] == unique_email

    def test_create_contact_invalid_token_returns_error(self):
        bad_context = {"env": {"INTERCOM_ACCESS_TOKEN": "invalid_token"}}
        expected_response = {
            "code": 401,
            "message": "Access Token Invalid",
            "status": "error",
        }
        cc = CreateContact({"email": "shawarma@hotgirl.com"}, bad_context)
        response = cc.execute()

        assert response == expected_response
