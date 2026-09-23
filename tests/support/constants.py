import os

CONTEXT = {
    "env": {
        "INTERCOM_ACCESS_TOKEN": os.environ.get("INTERCOM_ACCESS_TOKEN", "fake_token")
    }
}
