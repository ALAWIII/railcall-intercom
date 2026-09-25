from conftest import ConversationInfo
from handlers.api.conversations import DeleteConversation
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestDeleteConversation:
    """Tests for DeleteConversation endpoint."""

    def test_delete_conversation_success(self, class_conversation: ConversationInfo):
        """200: Successfully delete a conversation."""
        inputs = {"conversation_id": class_conversation.conversation_id}
        endpoint = DeleteConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()

        assert response["object"] == "conversation"
        assert response["id"] == class_conversation.conversation_id

    def test_delete_conversation_unauthorized(
        self, class_conversation: ConversationInfo
    ):
        """401: Invalid access token."""
        inputs = {"conversation_id": class_conversation.conversation_id}
        endpoint = DeleteConversation(inputs, {}, "invalid_token_12345")
        response = endpoint.execute()
        assert response["code"] == 401
