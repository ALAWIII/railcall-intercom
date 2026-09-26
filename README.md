# railcall-intercom

[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![RailCall](https://img.shields.io/badge/RailCall-Module-orange)](https://railcall.ai)
[![Intercom](https://img.shields.io/badge/Intercom-API-blue)](https://developers.intercom.com/)

A governed Intercom module for the [RailCall](https://railcall.ai) AI agent platform. This repository contains the source code, integration tests, and development documentation for the Intercom integration.

> **📦 End-User Documentation:** For marketplace features, installation instructions, and usage guides, please see **[docs/README.md](src/README.md)**.

## 📂 Project Structure

This project is organized to separate the **marketplace artifact** (`src/`) from the **development environment** (`tests/`, `docs/`).

```text
.
├── src/                            # 📦 The module shipped to the RailCall Marketplace
│   ├── handlers/                   # Python logic
│   │   ├── api/                    # Endpoint implementations
│   │   │   ├── admins/             # System/Admin endpoints (identify_admin)
│   │   │   ├── contacts/           # Contact management endpoints
│   │   │   └── conversations/      # Inbox/Conversation endpoints
│   │   ├── utils/                  # Shared utilities
│   │   │   ├── body_builder.py     # Constructs API payloads
│   │   │   ├── clean_response.py   # Strips noise from API responses for AI context
│   │   │   ├── error_handler.py    # Standardized error raising
│   │   │   ├── input_validator.py  # Business logic validation (RailCall convention)
│   │   │   ├── make_request.py     # HTTP request wrapper
│   │   │   └── url_builder.py      # URL and query param construction
│   │   └── handler.py              # Main entry point routing commands to classes
│   ├── module.json                 # RailCall manifest (schemas, permissions, security)
│   └── README.md                   # Marketplace-facing user documentation
├── tests/                          # 🧪 Pytest test suite
│   ├── api/                        # Integration tests for API endpoints
│   ├── support/                    # Test constants (e.g., token loading)
│   └── utils/                      # Unit tests for utility functions
├── conftest.py                     # Pytest fixtures (contacts, conversations, admin)
├── pytest.ini                      # Pytest configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🛠 Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ALAWIII/railcall-intercom.git
cd railcall-intercom
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

This project requires a live Intercom Access Token to run integration tests.

1.  Navigate to the [Intercom Developer Hub](https://developers.intercom.com/).
2.  Create a new App (or use an existing one).
3.  Under **Authentication**, generate an **Access Token**.
4.  Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```
5.  Add your token to `.env`:
    ```env
    INTERCOM_ACCESS_TOKEN=your_intercom_access_token_here
    ```

## 🧪 Running Tests

The test suite runs against the **live Intercom API**. Ensure your `.env` file is configured correctly before running tests.

**Run all tests:**

```bash
pytest
```

**Run with verbose output:**

```bash
pytest -v
```

**Run a specific test suite:**

```bash
# Contacts only
pytest tests/api/contacts

# Conversations only
pytest tests/api/conversations
```

**Run a specific test case:**

```bash
pytest tests/api/conversations/test_reply_conversation.py::TestReplyConversation::test_reply_conversation_success
```

## 🏗 Key Design Patterns & Architecture

This module was built with specific patterns to ensure safety and compatibility with the RailCall platform:

- **The Airlock Pattern:**
  - **Read Commands** (`list`, `show`, `identify`) are marked as `preview: false`. The AI agent can execute these silently to gather context.
  - **Write Commands** (`create`, `update`, `delete`, `reply`) are marked as `preview: true`. The RailCall platform intercepts these and requires explicit human approval before the API call is executed.

- **Input Validation:**
  - RailCall schemas are flat, but business logic often requires conditional validation (e.g., `admin_id` is required if `type` is `admin`).
  - The `InputValidator` utility enforces these rules _before_ the network request is made, preventing 400 errors from confusing the AI agent.

- **AI Context Optimization:**
  - Intercom API responses are large and contain structural noise (pagination cursors, internal links).
  - The `clean_response` utility strips this noise but intentionally preserves **domain types** (e.g., `"type": "conversation"`), giving the AI perfect context without wasting tokens.

- **RailCall Schema Compliance:**
  - `module.json` avoids JSON Schema pitfalls (no `properties` wrappers, no `boolean`/`integer` types) to ensure compatibility with the RailCall validator.

## 📝 Notes

- **Intercom API Version:** This module targets Intercom API version **2.16**.
- **Region Support:** The module supports US, EU, and AU Intercom workspaces (handled via the `INTERCOM_ACCESS_TOKEN` region configuration in Intercom).
- **Contest Entry:** This project was developed for the **RailCall Developer Challenge**.

## 🔗 Links

- [RailCall Documentation](https://railcall.ai/docs)
- [Intercom API Reference](https://developers.intercom.com/docs/references/rest-api/api.intercom.io)
