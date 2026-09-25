from handlers.api.conversations.base_conversations import BaseConversations
from handlers.utils import InputValidator, build_body

body_fields = [
    "message_type",
    "type",
    "admin_id",
    "body",
    "attachment_urls",
    "intercom_user_id",
    "email",
    "user_id",
]
exactly = [{"fields": ["conversation_id", "message_type", "type"], "count": 3}]


class ReplyConversation(BaseConversations):
    def __init__(self, inputs: dict, context: dict, token: str):
        # 1. Base validation
        InputValidator(inputs, exactly=exactly).validate()

        # 2. Conditional validation based on 'type'
        if inputs["type"] == "admin":
            InputValidator(
                inputs, exactly=[{"fields": ["admin_id"], "count": 1}]
            ).validate()
            if inputs["message_type"] not in ["note", "comment"]:
                raise RuntimeError(
                    "message_type must be 'note' or 'comment' when type is 'admin'."
                )
        elif inputs["type"] == "user":
            # Exactly ONE of these three must be provided
            InputValidator(
                inputs,
                exactly=[
                    {"fields": ["intercom_user_id", "email", "user_id"], "count": 1}
                ],
            ).validate()
            if inputs["message_type"] != "comment":
                raise RuntimeError(
                    "message_type must be 'comment' when type is 'user'."
                )
        else:
            raise RuntimeError("type must be 'admin' or 'user'")

        super().__init__(inputs, context, token)
        self.conversation_id = inputs["conversation_id"]
        self.url = f"{self.base_path}/{self.conversation_id}/reply"

        self.body = build_body(body_fields, inputs)

    def execute(self) -> dict:
        return self._make_request(self.url, "POST", self.body)
