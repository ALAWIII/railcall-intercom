from handlers.api.conversations.base_conversations import BaseConversations
from handlers.utils import InputValidator, build_url

path_parameters = ["conversation_id"]
query_parameters = ["display_as", "include_translations"]

exactly = [{"fields": path_parameters, "count": 1}]


class RetrieveConversation(BaseConversations):
    def __init__(self, inputs: dict, context: dict, token: str):
        InputValidator(inputs, exactly=exactly).validate()
        super().__init__(inputs, context, token)
        self.conversation_id: str = inputs["conversation_id"]
        self.url = build_url(
            f"{self.base_path}/{self.conversation_id}", query_parameters, inputs
        )

    def execute(self) -> dict:
        return self._make_request(self.url, "GET")
