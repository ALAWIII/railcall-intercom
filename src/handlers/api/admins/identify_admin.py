from handlers.api.admins.base_admins import BaseAdmins


class IdentifyAdmin(BaseAdmins):
    """Identify the currently authenticated admin."""

    def __init__(self, inputs: dict, context: dict, token: str):
        super().__init__(inputs, context, token)
        self.url = self.base_path

    def execute(self) -> dict:
        return self._make_request(self.url)
