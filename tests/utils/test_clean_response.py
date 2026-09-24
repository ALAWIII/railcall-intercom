import json

from handlers.utils import clean_response

input = json.loads("""
{
  "type": "contact",
  "id": "6ab2a35de5a3d1992a662a90",
  "workspace_id": "mud72027",
  "external_id": null,
  "role": "user",
  "email": "joebloggs@intercom.io",
  "email_domain": "intercom.io",
  "phone": null,
  "name": null,
  "avatar": null,
  "owner_id": null,
  "social_profiles": {
    "type": "list",
    "data": []
  },
  "has_hard_bounced": false,
  "marked_email_as_spam": false,
  "unsubscribed_from_emails": false,
  "created_at": 1790092125,
  "updated_at": 1790092125,
  "signed_up_at": null,
  "last_seen_at": null,
  "last_replied_at": null,
  "last_contacted_at": null,
  "last_email_opened_at": null,
  "last_email_clicked_at": null,
  "language_override": null,
  "browser": null,
  "browser_version": null,
  "browser_language": null,
  "os": null,
  "location": {
    "type": "location",
    "country": null,
    "region": null,
    "city": null,
    "country_code": null,
    "continent_code": null
  },
  "android_app_name": null,
  "android_app_version": null,
  "android_device": null,
  "android_os_version": null,
  "android_sdk_version": null,
  "android_last_seen_at": null,
  "ios_app_name": null,
  "ios_app_version": null,
  "ios_device": null,
  "ios_os_version": null,
  "ios_sdk_version": null,
  "ios_last_seen_at": null,
  "custom_attributes": {},
  "tags": {
    "type": "list",
    "data": [],
    "url": "/contacts/6ab2a35de5a3d1992a662a90/tags",
    "total_count": 0,
    "has_more": false
  },
  "notes": {
    "type": "list",
    "data": [],
    "url": "/contacts/6ab2a35de5a3d1992a662a90/notes",
    "total_count": 0,
    "has_more": false
  },
  "companies": {
    "type": "list",
    "data": [],
    "url": "/contacts/6ab2a35de5a3d1992a662a90/companies",
    "total_count": 0,
    "has_more": false
  },
  "opted_out_subscription_types": {
    "type": "list",
    "data": [],
    "url": "/contacts/6ab2a35de5a3d1992a662a90/subscriptions",
    "total_count": 0,
    "has_more": false
  },
  "opted_in_subscription_types": {
    "type": "list",
    "data": [],
    "url": "/contacts/6ab2a35de5a3d1992a662a90/subscriptions",
    "total_count": 0,
    "has_more": false
  },
  "utm_campaign": null,
  "utm_content": null,
  "utm_medium": null,
  "utm_source": null,
  "utm_term": null,
  "referrer": null,
  "sms_consent": false,
  "unsubscribed_from_sms": false,
  "enabled_push_messaging": null
}

""")
expected = json.loads("""

{
    "id": "6ab2a35de5a3d1992a662a90",
    "workspace_id": "mud72027",
    "role": "user",
    "email": "joebloggs@intercom.io",
    "email_domain": "intercom.io",
    "has_hard_bounced": false,
    "marked_email_as_spam": false,
    "unsubscribed_from_emails": false,
    "created_at": "2026-09-22T15:48:45+00:00",
    "updated_at": "2026-09-22T15:48:45+00:00",
    "tags": {"total_count": 0},
    "notes": {"total_count": 0},
    "companies": {"total_count": 0},
    "opted_out_subscription_types": {"total_count": 0},
    "opted_in_subscription_types": {"total_count": 0},
    "sms_consent": false,
    "unsubscribed_from_sms": false
}

""")


def test_clean_response():
    assert clean_response(input) == expected
