import os
import secrets
import sqlite3
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["DATABASE"] = str(Path(app.instance_path) / "users.sqlite3")


def get_db():
    if "db" not in g:
        Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                phone TEXT NOT NULL DEFAULT '',
                country TEXT NOT NULL DEFAULT '',
                password_hash TEXT NOT NULL
            )
            """
        )
        g.db.commit()
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def csrf_token():
    token = session.get("_csrf_token")
    if token is None:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


def validate_csrf():
    expected = session.get("_csrf_token", "")
    supplied = request.form.get("csrf_token", "")
    if not expected or not secrets.compare_digest(expected, supplied):
        abort(400, description="The form token is missing or invalid. Reload the page and try again.")


@app.context_processor
def inject_template_context():
    user_id = session.get("user_id")
    current_user = None
    if user_id is not None:
        current_user = get_db().execute(
            "SELECT id, full_name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    return {"csrf_token": csrf_token, "current_user": current_user}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = {}
    if request.method == "POST":
        validate_csrf()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        form = {"email": email}
        user = get_db().execute(
            "SELECT id, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Email or password is incorrect.", "error")
        else:
            session.clear()
            session["user_id"] = user["id"]
            flash("You are now logged in.", "success")
            return redirect(url_for("account"))

    return render_template("partials/_login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = {}
    if request.method == "POST":
        validate_csrf()
        form = {
            "full_name": request.form.get("full_name", "").strip(),
            "email": request.form.get("email", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "country": request.form.get("country", "").strip(),
        }
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not form["full_name"] or not form["email"] or "@" not in form["email"]:
            flash("Enter your name and a valid email address.", "error")
        elif len(password) < 8:
            flash("Your password must be at least 8 characters long.", "error")
        elif password != confirm_password:
            flash("The passwords do not match.", "error")
        else:
            db = get_db()
            try:
                cursor = db.execute(
                    """
                    INSERT INTO users (full_name, email, phone, country, password_hash)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        form["full_name"],
                        form["email"],
                        form["phone"],
                        form["country"],
                        generate_password_hash(password),
                    ),
                )
                db.commit()
            except sqlite3.IntegrityError:
                flash("An account with that email address already exists.", "error")
            else:
                session.clear()
                session["user_id"] = cursor.lastrowid
                flash("Your account has been created.", "success")
                return redirect(url_for("account"))

    return render_template("partials/_register.html", form=form)


@app.route("/account")
def account():
    user_id = session.get("user_id")
    if user_id is None:
        flash("Please log in to view your account.", "error")
        return redirect(url_for("login"))

    user = get_db().execute(
        "SELECT full_name, email, phone, country FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    if user is None:
        session.clear()
        flash("Your account could not be found. Please log in again.", "error")
        return redirect(url_for("login"))
    return render_template("partials/_accounts.html", user=user)


@app.route("/logout", methods=["POST"])
def logout():
    validate_csrf()
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.route("/submit-enquiry", methods=["POST"])
def submit_enquiry():
    validate_csrf()
    full_name = request.form.get("full_name", "").strip()
    contact = request.form.get("contact", "").strip()
    requirement = request.form.get("requirement", "").strip()
    if not full_name or not contact or not requirement:
        flash("Please complete all enquiry fields.", "error")
    else:
        flash("Thank you. Your enquiry has been received.", "success")
    return redirect(url_for("index", _anchor="enquiry"))


if __name__ == "__main__":
    app.run(debug=True)
