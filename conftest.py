import sys
from pathlib import Path

sys.dont_write_bytecode = True  # ← Prevents __pycache__ entirely

sys.path.insert(0, str(Path(__file__).parent / "src"))

# ====================== Fixtures
import uuid

import pytest

from handlers.api import CreateContact, CreateConversation
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class ContactInfo:
    def __init__(self, id: str, external_id: str, email: str):
        self.id = id
        self.external_id = external_id
        self.email = email


def create_test_contact() -> ContactInfo:
    if not INTERCOM_ACCESS_TOKEN:
        pytest.skip("Missing INTERCOM_ACCESS_TOKEN")

    unique = uuid.uuid4().hex

    inputs = {
        "email": f"railcall-{unique}@example.com",
        "external_id": f"railcall-{unique}",
    }

    response = CreateContact(inputs, {}, INTERCOM_ACCESS_TOKEN).execute()

    assert response.get("status") != "error", response
    assert response.get("id"), response

    return ContactInfo(response["id"], response["external_id"], response["email"])


@pytest.fixture(scope="class", name="class_contact")
def create_class_contact() -> ContactInfo:
    return create_test_contact()


@pytest.fixture(scope="function", name="function_contact")
def create_function_contact() -> ContactInfo:
    return create_test_contact()


# =================


class ConversationInfo:
    def __init__(self, response: dict, contact_nfo: ContactInfo):
        self.message_id = response["id"]
        self.conversation_id = response["conversation_id"]
        self.type = response["type"]
        self.message_type = response["message_type"]
        self.body = response["body"]
        self.contact_nfo = contact_nfo


def create_test_conversation():
    """Create a conversation to be deleted."""
    contact_info = create_test_contact()
    inputs = {
        "from_type": "user",
        "from_id": contact_info.id,
        "body": "Conversation to be deleted",
    }
    endpoint = CreateConversation(inputs, {}, INTERCOM_ACCESS_TOKEN)
    response = endpoint.execute()
    return ConversationInfo(response, contact_info)


@pytest.fixture(scope="function", name="function_conversation")
def create_function_conversation():
    return create_test_conversation()


@pytest.fixture(scope="class", name="class_conversation")
def create_class_conversation():
    return create_test_conversation()


# =====================


from handlers.api.admins import IdentifyAdmin


@pytest.fixture(scope="class", name="class_admin")
def fetch_class_admin():
    """Fetch the authenticated admin info."""
    endpoint = IdentifyAdmin({}, {}, INTERCOM_ACCESS_TOKEN)
    response = endpoint.execute()
    return response
