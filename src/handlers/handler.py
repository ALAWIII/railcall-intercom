import os

from handlers.api import (
    CreateContact,
    CreateConversation,
    DeleteContact,
    DeleteConversation,
    IdentifyAdmin,
    ListContacts,
    ListConversations,
    MergeContact,
    ReplyConversation,
    RetrieveConversation,
    ShowContact,
    UpdateContact,
    UpdateConversation,
)


def _get_intercom_access_token() -> str:
    try:
        creds = __rc_helpers__["vault_get"]("intercom1")  # type: ignore[name-defined]
        token = creds.get("INTERCOM_ACCESS_TOKEN")
    except NameError:
        token = os.environ.get("INTERCOM_ACCESS_TOKEN")

    if not token:
        raise ValueError("Missing INTERCOM_ACCESS_TOKEN")

    return token


# ======================================================== admins handlers


def intercom1_identify_admin(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return IdentifyAdmin(inputs, context, token).execute()


# ======================================================== contacts handlers


def intercom1_list_contacts(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return ListContacts(inputs, context, token).execute()


def intercom1_create_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return CreateContact(inputs, context, token).execute()


def intercom1_show_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return ShowContact(inputs, context, token).execute()


def intercom1_delete_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return DeleteContact(inputs, context, token).execute()


def intercom1_update_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return UpdateContact(inputs, context, token).execute()


def intercom1_merge_contact(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return MergeContact(inputs, context, token).execute()


# ======================================================== conversations handlers


def intercom1_list_conversations(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return ListConversations(inputs, context, token).execute()


def intercom1_delete_conversation(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return DeleteConversation(inputs, context, token).execute()


def intercom1_retrieve_conversation(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return RetrieveConversation(inputs, context, token).execute()


def intercom1_create_conversation(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return CreateConversation(inputs, context, token).execute()


def intercom1_update_conversation(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return UpdateConversation(inputs, context, token).execute()


def intercom1_reply_conversation(inputs: dict, context: dict) -> dict:
    token = _get_intercom_access_token()
    return ReplyConversation(inputs, context, token).execute()
