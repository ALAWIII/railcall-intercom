# Intercom Support Module for RailCall

Empower your AI agents to safely manage your Intercom support inbox and customer database.

Small support teams often drown in repetitive ticket triage. This module allows your AI to read your inbox, fetch customer history, and draft replies. Crucially, it wraps all destructive or outbound actions in a governed "airlock"—the AI drafts the action, but a human must explicitly approve it before anything is sent to a customer or deleted from your CRM.

## 🚀 Quick Start (Install & Setup)

Get up and running in under 5 minutes.

### 1. Install the Module

Run the following command in your RailCall CLI:

```bash
railcall market install agi87/intercom
```

### 2. Configure Credentials (The Trust Surface)

This module communicates directly with your live Intercom workspace. Your secrets are stored securely in your local RailCall vault and are **never** transmitted to external databases.

1. Log in to your [Intercom Developer Hub](https://developers.intercom.com/).
2. Go to **Your Apps** and create a new App (or use an existing one).
3. Navigate to **Authentication** and generate an **Access Token**.
4. Add this token to your RailCall vault environment variables as:
   `INTERCOM_ACCESS_TOKEN`

### 3. Verify Connection

Run the `intercom.identify_admin` command. If it returns your workspace name and your admin ID, your credentials are working perfectly.

## 🛠 Supported Commands

The module covers the top 13 essential actions for support operations.

**How the Airlock Works:**

- **Read Commands** run silently in the background. The AI uses these freely to gather context.
- **Write Commands** trigger a UI approval screen. The AI shows you exactly what it wants to change, and you must click "Approve" before the API call executes.

### 📥 Inbox & Conversations

| Command ID                       | Mode      | What it does                                                                              |
| :------------------------------- | :-------- | :---------------------------------------------------------------------------------------- |
| `intercom.list_conversations`    | **Read**  | Page through active, snoozed, and closed support tickets.                                 |
| `intercom.retrieve_conversation` | **Read**  | Fetch the full message thread, translations, and metadata for a specific ticket.          |
| `intercom.create_conversation`   | **Write** | Initiate a new support ticket on behalf of a user or lead.                                |
| `intercom.reply_conversation`    | **Write** | Draft a reply to a customer, or leave a private internal note for your team.              |
| `intercom.update_conversation`   | **Write** | Update ticket titles, mark as read, or attach custom attributes (e.g., `priority: high`). |
| `intercom.delete_conversation`   | **Write** | Permanently delete a spam or duplicate ticket.                                            |

### 👥 Contacts & CRM

| Command ID                | Mode      | What it does                                                                 |
| :------------------------ | :-------- | :--------------------------------------------------------------------------- |
| `intercom.list_contacts`  | **Read**  | Search and paginate through your user and lead database.                     |
| `intercom.show_contact`   | **Read**  | Fetch full profile data, tags, and company associations for a specific user. |
| `intercom.create_contact` | **Write** | Onboard a new lead or user into your Intercom workspace.                     |
| `intercom.update_contact` | **Write** | Update user attributes, emails, roles, or custom data points.                |
| `intercom.delete_contact` | **Write** | Permanently remove a contact from your database.                             |
| `intercom.merge_contact`  | **Write** | Deduplicate your CRM by safely merging two contact records together.         |

### ⚙️ System

| Command ID                | Mode     | What it does                                                                    |
| :------------------------ | :------- | :------------------------------------------------------------------------------ |
| `intercom.identify_admin` | **Read** | Verify connection and fetch the authenticated admin's ID and workspace details. |

## 🛡 Security & Guardrails

- **Zero-Trust Architecture:** The module requires a valid `INTERCOM_ACCESS_TOKEN` passed at runtime. The module author has zero access to your credentials or your workspace data.
- **Pagination Safety:** Intercom enforces strict limits on list endpoints. This module handles cursor-based pagination natively via the `starting_after` parameter, allowing the AI to safely scroll through thousands of records without hitting API limits.
- **Input Validation:** Complex Intercom payloads (like assigning a reply as an `admin` vs a `user`) are validated locally _before_ the network request is made, preventing malformed data from cluttering your logs.
