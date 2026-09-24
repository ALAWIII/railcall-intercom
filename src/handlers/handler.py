import os

from api import CreateContact, ListContacts


def _get_intercom_access_token() -> str:
    try:
        creds = __rc_helpers__["vault_get"]("intercom")  # type: ignore[name-defined]
        token = creds.get("INTERCOM_ACCESS_TOKEN")
    except NameError:
        token = os.environ.get("INTERCOM_ACCESS_TOKEN")

    if not token:
        raise ValueError("Missing INTERCOM_ACCESS_TOKEN")

    return token


# ======================================================== handlers


def intercom_list_contacts(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return ListContacts(inputs, context, token).execute()


def intercom_create_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return CreateContact(inputs, context, token).execute()
