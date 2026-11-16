import os, json, time
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")
CAPTURES = os.environ.get("CAPTURES", "/data/captures.jsonl")

@app.get("/")
def index():
    return send_from_directory(".", "index.html")

@app.post("/collect")
def collect():
    data = request.get_json(force=True, silent=True) or request.form.to_dict()
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
