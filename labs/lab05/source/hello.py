import base64
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    name   = request.args.get("name",   default="user", type=str)
    lastname = request.args.get("lastname", default="",   type=str)
    greeting = base64.b64decode(b"SGVsbG8gYXBwc2Vjd29ybGQ=").decode()
    tail     = f"@{name}" + (f" {lastname}" if lastname else "")
    return f"{greeting} from {tail}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
