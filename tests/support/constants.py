import os
from pathlib import Path

from dotenv import load_dotenv

# Find the project root (3 levels up from tests/support/constants.py)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")

intercom_token = os.getenv("INTERCOM_ACCESS_TOKEN")

INTERCOM_ACCESS_TOKEN = intercom_token if intercom_token else ""

if not INTERCOM_ACCESS_TOKEN:
    raise RuntimeError("INTERCOM_ACCESS_TOKEN not found. Please create a .env file.")
