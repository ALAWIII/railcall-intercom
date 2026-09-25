from handlers.api.conversations import UpdateConversation
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestUpdateConversation:
    """Tests for UpdateConversation endpoint."""

    def test_update_conversation_success(self, class_conversation):
        """200: Successfully update a conversation."""
        inputs = {
            "conversation_id": class_conversation.conversation_id,
            "title": "Updated test title",
        }
        endpoint = UpdateConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()

        assert response["type"] == "conversation"
        assert response["title"] == "Updated test title"

    def test_update_conversation_unauthorized(self, class_conversation):
        """401: Invalid access token."""
        inputs = {
            "conversation_id": class_conversation.conversation_id,
            "title": "Should fail",
        }
        endpoint = UpdateConversation(inputs, {}, "invalid_token_12345")
        response = endpoint.execute()
        assert response["code"] == 401

    def test_update_conversation_not_found(self):
        """404: Conversation not found."""
        inputs = {
            "conversation_id": 999999999999999,
            "title": "Should fail",
        }
        endpoint = UpdateConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()
        assert response["code"] == 404
