from conftest import ConversationInfo
from handlers.api.conversations import RetrieveConversation
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestRetrieveConversation:
    """Tests for RetrieveConversation endpoint."""

    def test_retrieve_conversation_success(self, class_conversation: ConversationInfo):
        """200: Successfully retrieve a conversation."""
        inputs = {"conversation_id": class_conversation.conversation_id}
        endpoint = RetrieveConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()

        assert response["type"] == "conversation"
        assert response["id"] == str(class_conversation.conversation_id)

    def test_retrieve_conversation_unauthorized(
        self, class_conversation: ConversationInfo
    ):
        """401: Invalid access token."""
        inputs = {"conversation_id": class_conversation.conversation_id}
        endpoint = RetrieveConversation(inputs, {}, "invalid_token_12345")
        response = endpoint.execute()
        assert response["code"] == 401

    def test_retrieve_conversation_not_found(self):
        """404: Conversation not found."""
        inputs = {"conversation_id": 999999999999999}
        endpoint = RetrieveConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()
        assert response["code"] == 404
