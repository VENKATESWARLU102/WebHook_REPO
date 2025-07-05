from flask import Blueprint, request, jsonify
from app.extensions import mongo
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    payload = request.json

    # Detect action type
    if "head_commit" in payload:
        # It's a PUSH
        action_type = "PUSH"
        request_id = payload["head_commit"]["id"]
        author = payload["head_commit"]["author"]["name"]
        from_branch = payload["ref"].split("/")[-1]
        to_branch = from_branch  # PUSH doesn't change branch
        timestamp = payload["head_commit"]["timestamp"]
    elif "pull_request" in payload:
        action_type = "MERGE" if payload["action"] == "closed" and payload["pull_request"].get("merged") else "PULL_REQUEST"
        request_id = str(payload["pull_request"]["id"])
        author = payload["pull_request"]["user"]["login"]
        from_branch = payload["pull_request"]["head"]["ref"]
        to_branch = payload["pull_request"]["base"]["ref"]
        timestamp = payload["pull_request"]["updated_at"]
    else:
        return jsonify({"status": "ignored", "message": "Unsupported event type"}), 200

    # Format to match MongoDB schema
    document = {
        "request_id": request_id,
        "author": author,
        "action": action_type,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ") if "Z" in timestamp else timestamp,
    }

    mongo.db.webhook_events.insert_one(document)
    return jsonify({"status": "success"}), 200

@webhook.route('/events', methods=["GET"])
def get_events():
    events = []
    for doc in mongo.db.webhook_events.find().sort("timestamp", -1).limit(20):
        events.append({
            "request_id": doc.get("request_id"),
            "author": doc.get("author"),
            "action": doc.get("action"),
            "from_branch": doc.get("from_branch"),
            "to_branch": doc.get("to_branch"),
            "timestamp": doc.get("timestamp").isoformat() if hasattr(doc.get("timestamp"), "isoformat") else str(doc.get("timestamp")),
        })
    return jsonify(events)
