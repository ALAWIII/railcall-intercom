import sys
from pathlib import Path

sys.dont_write_bytecode = True  # ← Prevents __pycache__ entirely

sys.path.insert(0, str(Path(__file__).parent / "src"))

# ====================== Fixtures
import uuid

import pytest

from handlers.api.contacts import CreateContact
from tests.support.constants import INTERCOM_ACCESS_TOKEN


class ContactInfo:
    def __init__(self, id: str, external_id: str, email: str):
        self.id = id
        self.external_id = id
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


@pytest.fixture(scope="class", name="function_contact")
def create_function_contact() -> ContactInfo:
    return create_test_contact()
