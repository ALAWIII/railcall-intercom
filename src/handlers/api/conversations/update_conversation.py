from handlers.api.conversations.base_conversations import BaseConversations
from handlers.utils import InputValidator, build_body, build_url

path_parameters = ["conversation_id"]
query_parameters = ["display_as"]
body_fields = ["read", "title", "custom_attributes", "company_id"]

exactly = [{"fields": ["conversation_id"], "count": 1}]


class UpdateConversation(BaseConversations):
    def __init__(self, inputs: dict, context: dict, token: str):
        InputValidator(inputs, exactly=exactly).validate()
        super().__init__(inputs, context, token)

        self.conversation_id = inputs["conversation_id"]
        self.url = build_url(
            f"{self.base_path}/{self.conversation_id}", query_parameters, inputs
        )
        self.body = build_body(body_fields, inputs)

    def execute(self) -> dict:
        return self._make_request(self.url, "PUT", self.body)
