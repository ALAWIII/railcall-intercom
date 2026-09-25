from handlers.api.conversations.base_conversations import BaseConversations
from handlers.utils import InputValidator, build_body

body_fields = ["from", "body", "subject", "attachment_urls", "created_at", "brand_id"]

exactly = [{"fields": ["from_id", "from_type", "body"], "count": 3}]


class CreateConversation(BaseConversations):
    def __init__(self, inputs: dict, context: dict, token: str):
        InputValidator(inputs, exactly=exactly).validate()
        if inputs["from_type"] not in ["lead", "user", "contact"]:
            raise RuntimeError("from_type must be one of: lead, user, contact")
        inputs["from"] = {"type": inputs["from_type"], "id": inputs["from_id"]}
        super().__init__(inputs, context, token)
        self.url = f"{self.base_path}"
        self.body = build_body(body_fields, inputs)

    def execute(self) -> dict:
        return self._make_request(self.url, "POST", self.body)
