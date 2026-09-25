import os

from api import (
    CreateContact,
    DeleteContact,
    ListContacts,
    MergeContact,
    ShowContact,
    UpdateContact,
)


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


def intercom_show_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return ShowContact(inputs, context, token).execute()


def intercom_delete_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return DeleteContact(inputs, context, token).execute()


def intercom_update_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return UpdateContact(inputs, context, token).execute()


def intercom_merge_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return MergeContact(inputs, context, token).execute()
