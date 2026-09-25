from handlers.api.conversations import ReplyConversation
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestReplyConversation:
    """Tests for ReplyConversation endpoint."""

    def test_reply_conversation_success(self, class_conversation, class_admin):
        """200: Successfully reply to a conversation as admin."""
        inputs = {
            "conversation_id": class_conversation.conversation_id,
            "message_type": "note",
            "type": "admin",
            "admin_id": class_admin["id"],
            "body": "Test internal note",
        }
        endpoint = ReplyConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()

        assert response["type"] == "conversation"
        assert response["id"] == str(class_conversation.conversation_id)

    def test_reply_conversation_unauthorized(self, class_conversation, class_admin):
        """401: Invalid access token."""
        inputs = {
            "conversation_id": class_conversation.conversation_id,
            "message_type": "note",
            "type": "admin",
            "admin_id": class_admin["id"],
            "body": "Should fail",
        }
        endpoint = ReplyConversation(inputs, {}, "invalid_token_12345")
        response = endpoint.execute()
        assert response["code"] == 401

    def test_reply_conversation_not_found(self, class_admin):
        """404: Conversation not found."""
        inputs = {
            "conversation_id": 999999999999999,
            "message_type": "note",
            "type": "admin",
            "admin_id": class_admin["id"],
            "body": "Should fail",
        }
        endpoint = ReplyConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()
        assert response["code"] == 404
