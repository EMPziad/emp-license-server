from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

LICENSE_FILE = "licenses.json"

def load_licenses():
    try:
        with open(LICENSE_FILE, "r") as f:
            return json.load(f)
    except:
        return []

@app.route("/verify", methods=["POST"])
def verify_license():
    try:
        payload = request.json
        device = payload.get("device")
        expiry = payload.get("expiry")

        licenses = load_licenses()

        for lic in licenses:
            if lic["device"] == device and lic["expiry"] == expiry:
                # Check if still valid
                if datetime.strptime(expiry, "%Y-%m-%d") >= datetime.now():
                    return jsonify({"status": "valid"})

        return jsonify({"status": "invalid"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
