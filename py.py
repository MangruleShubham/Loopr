from flask import Flask, request, jsonify
import jwt
import json

app = Flask(__name__)

# Load user data from a JSON file
with open("loopr/users.json") as f:
    users = json.load(f)

# Secret key for JWT
app.config["SECRET_KEY"] = "Shubham@1312"

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return jsonify({"message": "Invalid username or password"}), 400

    # Check if the username and password match
    if username in users and users[username] == password:
        # Generate a JWT token
        token = jwt.encode({"username": username}, app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"token": token}), 200

    return jsonify({"message": "Invalid username or password"}), 401

@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        # Verify and decode the JWT token
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        username = payload["username"]

        return jsonify({"message": f"Welcome, {username}! This is a protected route."}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(debug=True)
