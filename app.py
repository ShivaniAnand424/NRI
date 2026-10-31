import os
import secrets
import sqlite3
from pathlib import Path
from urllib.parse import urlsplit

from flask import (
    Flask,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from csrf import csrf_token, validate_csrf
from service_routes import service_pages

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
app.config["DATABASE"] = str(Path(app.instance_path) / "users.sqlite3")

# Contact details used by the site-visit band and the property cards.
SITE = {
    "phone_display": "+91 00000 00000",
    "phone_link": "+910000000000",      # + and digits only
    "whatsapp_number": "910000000000",  # digits only, with country code
}

# Add only real, approved listings here (with the owner's/developer's permission).
# Put the photo in static/images/properties/ and use its file name below.
PROPERTIES = [
    # {
    #     "name": "Project name",
    #     "location": "Area, Nagpur",
    #     "type": "2 & 3 BHK apartments",
    #     "price": "From ₹00 lakh",
    #     "rera": "P50000000000",          # optional
    #     "image": "project-name.jpg",
    #     "alt": "Exterior view of Project name in Area, Nagpur",
    # },
]


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
        g.db.execute(
            """
            CREATE TABLE IF NOT EXISTS service_enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                service_slug TEXT NOT NULL,
                responses_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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


@app.context_processor
def inject_template_context():
    user_id = session.get("user_id")
    current_user = None
    if user_id is not None:
        current_user = get_db().execute(
            "SELECT id, full_name, email FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    return {"csrf_token": csrf_token, "current_user": current_user, "site": SITE}


def safe_next_url(target):
    if not target or "\\" in target:
        return None

    parsed = urlsplit(target)
    if (
        parsed.scheme
        or parsed.netloc
        or not parsed.path.startswith("/")
        or parsed.path.startswith("//")
    ):
        return None
    return target


@app.route("/")
def index():
    return render_template("index.html", properties=PROPERTIES)


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
            return redirect(safe_next_url(request.form.get("next", "")) or url_for("account"))

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
                return redirect(safe_next_url(request.form.get("next", "")) or url_for("account"))

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


app.register_blueprint(service_pages)


if __name__ == "__main__":
    app.run(debug=True)