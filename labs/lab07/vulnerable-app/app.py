from flask import Flask, request, make_response, jsonify
import sqlite3
import os
import subprocess
import json
import logging
import ast
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Fix: Disable DEBUG mode in production
app.config["DEBUG"] = False

# Fix: Move credentials to environment variables
DB_USER = os.environ.get("DB_USER", "user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "changeme")
DB_PATH = "app.db"

# Fix: Set logging level to INFO instead of DEBUG
logging.basicConfig(level=logging.INFO)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn


@app.route("/")
def index():
    # Fix: Remove version disclosure
    return "Lab07 Security-Enhanced Application"


@app.route("/user")
def get_user():
    username = request.args.get("name", "")
    conn = get_db()
    cur = conn.cursor()
    # Fix: Use parameterized query to prevent SQL injection
    query = "SELECT id, name, email FROM users WHERE name = ?"
    app.logger.info("Fetching user data")  # Fix: Don't log query details
    rows = cur.execute(query, (username,)).fetchall()
    conn.close()
    return {"result": rows}


@app.route("/search")
def search():
    q = request.args.get("q", "")
    # Fix: Escape user input to prevent XSS
    safe_q = escape(q)
    html = f"<h1>Results for: {safe_q}</h1>"
    return make_response(html, 200)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # Fix: Validate input and use subprocess.run with list arguments
    # Only allow alphanumeric, dots, and hyphens for hostnames/IPs
    if not all(c.isalnum() or c in ".-" for c in host):
        return "Invalid host format", 400
    if len(host) > 255:
        return "Host too long", 400

    try:
        # Fix: Use subprocess.run with list args to prevent command injection
        result = subprocess.run(
            ["/bin/ping", "-c", "1", "-W", "2", host],
            capture_output=True,
            text=True,
            timeout=5
        )
        return f"Ping result: {result.returncode}"
    except subprocess.TimeoutExpired:
        return "Ping timeout", 408
    except Exception as e:
        app.logger.error("Ping error")
        return "Ping failed", 500


@app.route("/backup")
def backup():
    # Fix: Remove this dangerous endpoint or restrict access
    # For now, disable functionality
    return "Backup functionality has been disabled for security", 403


@app.route("/read")
def read_file():
    # Fix: Restrict file access to allowed directory and use secure_filename
    filename = request.args.get("filename", "")
    if not filename:
        return "Filename required", 400

    # Only allow reading from /tmp/safe_files directory
    safe_dir = "/tmp/safe_files"
    safe_name = secure_filename(filename)
    full_path = os.path.join(safe_dir, safe_name)

    # Ensure path doesn't escape safe directory
    if not os.path.abspath(full_path).startswith(os.path.abspath(safe_dir)):
        return "Access denied", 403

    try:
        if not os.path.exists(full_path):
            return "File not found", 404
        with open(full_path, "r") as f:
            data = f.read()
        return f"<pre>{escape(data)}</pre>"
    except Exception as e:
        app.logger.error("File read error")
        return "Error reading file", 500


@app.route("/load")
def load():
    data = request.args.get("data", "")
    try:
        # Fix: Use JSON instead of pickle for deserialization
        obj = json.loads(data)
        return jsonify({"loaded_object": obj})
    except json.JSONDecodeError as e:
        return "Invalid JSON data", 400
    except Exception as e:
        app.logger.error("Load error")
        return "Error loading data", 500


@app.route("/calc")
def calc():
    expr = request.args.get("expr", "1+1")
    try:
        # Fix: Use ast.literal_eval for safe evaluation (only literals)
        result = ast.literal_eval(expr)
        return str(result)
    except (ValueError, SyntaxError):
        return "Invalid expression. Only numeric literals allowed", 400
    except Exception as e:
        app.logger.error("Calc error")
        return "Calculation error", 500


# Fix: Remove debug endpoint that exposes sensitive information
# @app.route("/debug")
# def debug():
#     This endpoint has been removed for security


if __name__ == "__main__":
    # Fix: Bind to localhost instead of 0.0.0.0
    app.run(host="127.0.0.1", port=8080)
