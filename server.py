import os
import json
import time
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024

CAPTURES = os.environ.get("CAPTURES", "/data/captures.jsonl")


@app.after_request
def harden(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["X-Frame-Options"] = "DENY"
    return resp


@app.get("/")
def index():
    return send_from_directory(".", "index.html")


@app.post("/collect")
def collect():
    data = request.get_json(silent=True) or request.form.to_dict()
    if not isinstance(data, dict):
        return jsonify(ok=False, error="bad payload"), 400

    rec = {
        "ts": time.time(),
        "ip": request.remote_addr,
        "ua": request.headers.get("User-Agent"),
        "data": data,
    }

    os.makedirs(os.path.dirname(CAPTURES), exist_ok=True)
    with open(CAPTURES, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    return jsonify(ok=True)


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=False)
