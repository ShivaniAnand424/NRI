import os
import secrets
import smtplib
from email.message import EmailMessage
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
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
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from csrf import csrf_token, validate_csrf
from database import get_db, init_app as init_database
from service_routes import service_pages

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
Path(app.instance_path).mkdir(parents=True, exist_ok=True)
app.config["DATABASE_URL"] = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{(Path(app.instance_path) / 'users.sqlite3').as_posix()}",
)
init_database(app)

# Contact details used by the site-visit band and the property cards.
SITE = {
    "phone_display": "+91 78750 06655",
    "phone_link": "+917875006655",
    "phone2_display": "+91 78750 06633",
    "phone2_link": "+917875006633",
    "whatsapp_number": "917875006655",  # digits only, with country code
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
            text("SELECT id, full_name, email FROM users WHERE id = :user_id"),
            {"user_id": user_id},
        ).mappings().first()
    return {"csrf_token": csrf_token, "current_user": current_user, "site": SITE}


def send_enquiry_email(details):
    """Emails a copy of a new enquiry to the team.

    Works only when these environment variables are set:
    SMTP_HOST, SMTP_USER, SMTP_PASSWORD, ENQUIRY_EMAIL_TO
    (SMTP_PORT is optional, default 587). Otherwise it quietly does nothing.
    """
    host = os.environ.get("SMTP_HOST")
    user = os.environ.get("SMTP_USER")
    password = os.environ.get("SMTP_PASSWORD")
    recipient = os.environ.get("ENQUIRY_EMAIL_TO")
    if not (host and user and password and recipient):
        return False

    message = EmailMessage()
    message["Subject"] = f"New NRIPMC enquiry from {details['full_name']}"
    message["From"] = user
    message["To"] = recipient
    message.set_content(
        "A new enquiry was received on the website.\n\n"
        f"Name: {details['full_name']}\n"
        f"Contact: {details['contact']}\n"
        f"Property location: {details['property_location'] or '-'}\n"
        f"Service: {details['service'] or '-'}\n\n"
        f"Message:\n{details['requirement']}\n"
    )
    try:
        with smtplib.SMTP(host, int(os.environ.get("SMTP_PORT", "587")), timeout=15) as server:
            server.starttls()
            server.login(user, password)
            server.send_message(message)
        return True
    except Exception:
        app.logger.exception("Could not send the enquiry email")
        return False


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


@app.route("/our-services")
def our_services():
    return render_template("services.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = {}
    if request.method == "POST":
        validate_csrf()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        form = {"email": email}
        user = get_db().execute(
            text("SELECT id, password_hash FROM users WHERE email = :email"),
            {"email": email},
        ).mappings().first()

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
                    text("""
                    INSERT INTO users (full_name, email, phone, country, password_hash)
                    VALUES (:full_name, :email, :phone, :country, :password_hash)
                    """),
                    {
                        "full_name": form["full_name"],
                        "email": form["email"].lower(),
                        "phone": form["phone"],
                        "country": form["country"],
                        "password_hash": generate_password_hash(password),
                    },
                )
                db.commit()
            except IntegrityError:
                db.rollback()
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
        text("SELECT full_name, email, phone, country FROM users WHERE id = :user_id"),
        {"user_id": user_id},
    ).mappings().first()
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
    property_location = request.form.get("property_location", "").strip()
    service = request.form.get("service", "").strip()
    if not full_name or not contact or not requirement:
        flash("Please complete all enquiry fields.", "error")
    else:
        details = {
            "full_name": full_name,
            "contact": contact,
            "property_location": property_location,
            "service": service,
            "requirement": requirement,
        }
        db = get_db()
        db.execute(
            text("""
            INSERT INTO enquiries
                (full_name, contact, property_location, service, requirement, source_page)
            VALUES (:full_name, :contact, :property_location, :service, :requirement, :source_page)
            """),
            {
                "full_name": full_name,
                "contact": contact,
                "property_location": property_location,
                "service": service,
                "requirement": requirement,
                "source_page": (request.referrer or "")[:200],
            },
        )
        db.commit()
        send_enquiry_email(details)
        flash("Thank you. Your enquiry has been received.", "success")
    return redirect(
        safe_next_url(request.form.get("next", ""))
        or url_for("index", _anchor="enquiry")
    )


app.register_blueprint(service_pages)


if __name__ == "__main__":
    app.run(debug=True)