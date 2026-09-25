from handlers.api.conversations.base_conversations import BaseConversations
from handlers.utils import build_url

query_parameters = ["starting_after", "per_page"]


class ListConversations(BaseConversations):
    def __init__(self, inputs: dict, context: dict, token: str):
        super().__init__(inputs, context, token)
        self.url = build_url(self.base_path, query_parameters, inputs)

    def execute(self) -> dict:
        return self._make_request(self.url)
