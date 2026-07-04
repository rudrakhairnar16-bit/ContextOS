from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["SECRET"] = "your-secret-key"

# BUG: JWT token not refreshing on /api/auth/refresh
# Current status: Unsolved
# Tried: sliding window (failed - tokens expired mid-session)
# Tried: forced re-login (bad UX)
# Next: try token rotation approach

users_db = {
    "admin": {"password": "admin123", "role": "admin"},
    "dev": {"password": "dev123", "role": "developer"}
}

def create_token(username):
    return jwt.encode(
        {"sub": username, "exp": datetime.utcnow() + timedelta(hours=1)},
        app.config["SECRET"],
        algorithm="HS256"
    )

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = users_db.get(data.get("username"))
    if user and user["password"] == data.get("password"):
        return jsonify({"token": create_token(data["username"])})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/auth/refresh", methods=["POST"])
def refresh():
    # TODO: Implement token rotation
    # Current approach doesn't work
    return jsonify({"error": "Not implemented"}), 501

if __name__ == "__main__":
    app.run(port=5000)
