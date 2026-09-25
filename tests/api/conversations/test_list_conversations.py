from handlers.api.conversations import ListConversations
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class TestListConversations:
    """Tests for ListConversations endpoint."""

    def test_list_conversations_success(self):
        """200: Successfully list conversations."""
        inputs = {"per_page": 5}
        endpoint = ListConversations(inputs, {}, INTERCOM_ACCESS_TOKEN)
        response = endpoint.execute()

        assert response["type"] == "conversation.list"
        assert "conversations" in response
        assert "pages" in response

    def test_list_conversations_unauthorized(self):
        """401: Invalid access token."""
        inputs = {"per_page": 5}
        endpoint = ListConversations(inputs, {}, "invalid_token_12345")
        response = endpoint.execute()
        assert response["code"] == 401
