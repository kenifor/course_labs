from flask import (
    Flask,
    request,
    make_response,
    render_template_string,
    redirect,
    url_for,
)
import sqlite3
import os
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(32))

DB_PATH = os.environ.get("APP_DB_PATH", "app.db")

# Security headers middleware
@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response


def hash_password(password):
    """Simple password hashing using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            role TEXT
        )
        """
    )
    cur.execute("DELETE FROM users")
    # Use environment variables for credentials and hash passwords
    admin_pass = os.environ.get("ADMIN_PASSWORD", "admin123")
    user_pass = os.environ.get("USER_PASSWORD", "user123")
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ('admin', hash_password(admin_pass), 'admin')
    )
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        ('user', hash_password(user_pass), 'user')
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    html = """
    <h1>Vulnerable DAST Demo App</h1>
    <p>Пример уязвимого приложения для лабораторной по DAST.</p>
    <ul>
      <li><a href="/echo?msg=Hello">Reflected XSS / echo</a></li>
      <li><a href="/search?username=admin">SQL Injection / search</a></li>
      <li><a href="/login">Небезопасный логин</a></li>
      <li><a href="/profile">Профиль (зависит от cookie)</a></li>
      <li><a href="/admin">«Админка» без нормальной авторизации</a></li>
      <li><a href="/files/">Directory listing</a></li>
    </ul>
    """
    resp = make_response(html)
    resp.set_cookie("session", "guest-session-id", httponly=True, secure=True, samesite='Lax')
    return resp


@app.route("/echo")
def echo():
    msg = request.args.get("msg", "")
    # Use Jinja2 auto-escaping to prevent XSS
    template = """
    <h2>Echo</h2>
    <p>Сообщение: {{ msg }}</p>
    <p>Попробуйте передать что-нибудь вроде: <code>&lt;script&gt;alert('XSS')&lt;/script&gt;</code></p>
    <a href="/">Назад</a>
    """
    return render_template_string(template, msg=msg)


@app.route("/search")
def search():
    username = request.args.get("username", "")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Use parameterized queries to prevent SQL injection
    query = "SELECT id, username, role FROM users WHERE username = ?"
    rows = []
    error = None
    try:
        for row in cur.execute(query, (username,)):
            rows.append(row)
    except Exception as e:
        error = str(e)

    conn.close()

    template = """
    <h2>Поиск пользователя</h2>
    <p>Запрос: <code>{{ query }}</code></p>
    {% if error %}
      <p style="color:red;">SQL error: {{ error }}</p>
    {% endif %}
    {% if rows %}
      <ul>
      {% for id, username, role in rows %}
        <li>{{ id }} – {{ username }} ({{ role }})</li>
      {% endfor %}
      </ul>
    {% else %}
      <p>Ничего не найдено</p>
    {% endif %}
    <p>Попробуйте, например: <code>?username=admin' OR '1'='1</code></p>
    <a href="/">Назад</a>
    """
    return render_template_string(template, query=query, rows=rows, error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        form = """
        <h2>Логин</h2>
        <form method="post">
          <label>Username: <input type="text" name="username"></label><br>
          <label>Password: <input type="password" name="password"></label><br>
          <button type="submit">Login</button>
        </form>
        <p>Попробуйте: admin / admin123 или user / user123</p>
        <a href="/">Назад</a>
        """
        return render_template_string(form)

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Use parameterized queries and hash password
    query = "SELECT id, username, role FROM users WHERE username = ? AND password = ?"
    row = cur.execute(query, (username, hash_password(password))).fetchone()
    conn.close()

    if row:
        _, uname, role = row
        # Create server-side session token instead of storing role in cookie
        session_token = secrets.token_hex(16)
        resp = make_response(
            f"<h2>Добро пожаловать, {uname} ({role})!</h2><a href='/'>На главную</a>"
        )

        resp.set_cookie("user", uname, httponly=True, secure=True, samesite='Lax')
        resp.set_cookie("role", role, httponly=True, secure=True, samesite='Lax')
        resp.set_cookie("session_token", session_token, httponly=True, secure=True, samesite='Lax')
        return resp
    else:
        return render_template_string(
            "<h2>Неверные учетные данные</h2><a href='/login'>Попробовать снова</a>"
        )


@app.route("/profile")
def profile():
    username = request.cookies.get("user", "guest")
    role = request.cookies.get("role", "guest")

    template = """
    <h2>Профиль пользователя</h2>
    <p>Имя: {{ username }}</p>
    <p>Роль: {{ role }}</p>
    <p>Cookie легко подделать: можно выдать себе роль 'admin'.</p>
    <a href="/">Назад</a>
    """
    return render_template_string(template, username=username, role=role)


@app.route("/admin")
def admin():
    role = request.cookies.get("role", "guest")
    if role != "admin":
        return (
            "<h2>Доступ запрещён: вы не admin</h2><p>Попробуйте изменить cookie 'role'.</p><a href='/'>Назад</a>",
            403,
        )

    template = """
    <h2>Admin panel</h2>
    <p>Секретные настройки приложения (демо).</p>
    <ul>
      <li>DEBUG: true</li>
      <li>FEATURE_FLAG: experimental_mode</li>
    </ul>
    <a href="/">Назад</a>
    """
    return render_template_string(template)


@app.route("/files/")
@app.route("/files/<path:subpath>")
def files(subpath=""):
    # Whitelist of allowed files to prevent directory traversal and listing
    ALLOWED_FILES = []  # Empty list - disable file access completely for security
    # Or use: ALLOWED_FILES = ['public_file.txt'] to allow specific files

    base_dir = os.path.abspath(os.path.dirname(__file__))
    target_dir = os.path.join(base_dir, "files")

    # Prevent directory traversal
    full_path = os.path.abspath(os.path.join(target_dir, subpath))
    if not full_path.startswith(target_dir):
        return "<h2>Доступ запрещён</h2><a href='/'>Назад</a>", 403

    if not os.path.exists(full_path):
        return "<h2>Путь не найден</h2><a href='/'>Назад</a>", 404

    # Disable directory listing for security
    if os.path.isdir(full_path):
        return "<h2>Доступ к директориям запрещён</h2><a href='/'>Назад</a>", 403

    # Check if file is in whitelist
    if subpath not in ALLOWED_FILES:
        return "<h2>Доступ к этому файлу запрещён</h2><a href='/'>Назад</a>", 403

    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return f"<pre>{content}</pre>"


if __name__ == "__main__":
    init_db()
    # Disable debug mode in production
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    app.run(host="0.0.0.0", port=8080, debug=debug_mode)
