# WebHook_REPO

GitHub Webhook Setup

Created a GitHub repository called action-repo to simulate activity (e.g., push, pull request, merge).

Configured a GitHub webhook to send a POST request to an external server whenever a push or pull_request event occurs.

Webhook Receiver (Flask Backend)

Created another repository called webhook-repo which contains the Flask application to receive and handle webhook payloads.

Since Flask runs locally (on localhost), used ngrok to expose it to the internet, and copied the ngrok public URL to GitHub webhook settings.

This allows GitHub to send webhook events from action-repo to the local Flask server via ngrok.

Webhook Payload Handling

The Flask server receives the raw JSON payload from GitHub.

It determines:

If it’s a push event → extracts commit info (author, ID, branch, timestamp).

If it’s a pull request, it checks if the PR is merged or just opened/updated.

Constructs a structured document with these fields:
request_id, author, action, from_branch, to_branch, timestamp.

MongoDB Integration

![WhatsApp Image 2025-07-05 at 17 14 29_6a624f02](https://github.com/user-attachments/assets/667bac1c-1b9c-4470-a9ee-d22734c4ae53)


The structured data is stored in MongoDB using the schema specified in the task.

This allows for querying and displaying a history of GitHub actions.

Frontend (UI)

The UI periodically (every 15 seconds) polls MongoDB for new events using an endpoint.

Displays a minimal, clean interface showing recent actions like PUSH, PULL_REQUEST, and MERGE along with relevant metadata (author, branches, time).
