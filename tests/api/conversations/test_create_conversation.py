from handlers.api.conversations import CreateConversation
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestCreateConversation:
    """Tests for CreateConversation endpoint."""

    def test_create_conversation_success(self, class_contact):
        """200: Successfully create a conversation."""
        inputs = {
            "from_type": "user",
            "from_id": class_contact.id,
            "body": "Test conversation from pytest",
        }
        endpoint = CreateConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()

        assert response["type"] == "user_message"
        assert response["body"] == "Test conversation from pytest"
        assert "conversation_id" in response
        assert "id" in response

    def test_create_conversation_unauthorized(self, class_contact):
        """401: Invalid access token."""
        inputs = {
            "from_type": "user",
            "from_id": class_contact.id,
            "body": "Should fail",
        }
        endpoint = CreateConversation(inputs, {}, "invalid_token_12345")
        response = endpoint.execute()
        assert response["code"] == 401

    def test_create_conversation_not_found(self):
        """404: Contact not found."""
        inputs = {
            "from_type": "user",
            "from_id": "000000000000000000000000",
            "body": "Should fail - user not found",
        }
        endpoint = CreateConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()
        assert response["code"] == 404
