import uuid
from pprint import pprint

from handlers.contacts import CreateContact
from tests.support.constants import CONTEXT


class TestCreateContact:
    def test_create_contact_returns_200(self):
        # Generate unique email for each test run
        unique_email = f"test-{uuid.uuid4()}@example.com"

        cc = CreateContact({"email": unique_email}, CONTEXT)
        response = cc.execute()
        pprint(response)
        # Assert success
        assert "status" not in response or response.get("status") != "error"

        assert "id" in response
        # "Assert contact was created"
        assert response["email"] == unique_email
