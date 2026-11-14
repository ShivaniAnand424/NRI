import os
import secrets
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

from about import COMPANIES, LEADERS, STATS, TEAM, VALUES
from csrf import csrf_token, validate_csrf
from database import get_db, init_app as init_database
from notify import send_alert
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
    {
        "name": "Nirmal Keshavam-15",
        "location": "Nagpur, Maharashtra",
        "type": "Residential plotted layout",
        "price": "Sold / fully transacted",
        "image": "keshavam-15.jpg",
        "alt": "Nirmal Keshavam-15 residential layout brochure cover",
    },
    {
        "name": "Keshavam City-11",
        "location": "Nagpur, Maharashtra",
        "type": "Residential plotted layout",
        "price": "Sold / fully transacted",
        "image": "keshavam-city-11.jpg",
        "alt": "Keshavam City-11 residential layout brochure cover",
    },
    {
        "name": "Saraswati Nagar-3",
        "location": "Mouza Rui, Nagpur (Gramin)",
        "type": "RERA residential layout",
        "price": "Sold / fully transacted",
        "image": "saraswati-nagar-3.jpg",
        "alt": "Saraswati Nagar-3 residential layout brochure cover",
    },
    {
        "name": "Sai Pride-III",
        "location": "Manewada, Nagpur",
        "type": "1, 2 & 3 BHK luxury flats",
        "price": "Sold / fully transacted",
        "image": "sai-pride-iii.jpg",
        "alt": "Sai Pride-III luxury apartment brochure cover",
    },
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


@app.route("/about")
def about():
    return render_template(
        "about.html",
        stats=STATS,
        leaders=LEADERS,
        companies=COMPANIES,
        values=VALUES,
        team=TEAM,
    )


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
                send_alert(
                    f"New NRIPMC account: {form['full_name']}",
                    "A new customer registered on the website.\n\n"
                    f"Name: {form['full_name']}\n"
                    f"Email: {form['email']}\n"
                    f"Phone: {form['phone'] or '-'}\n"
                    f"Country: {form['country'] or '-'}\n",
                )
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
        send_alert(
            f"New NRIPMC enquiry from {full_name}",
            "A new enquiry was received on the website.\n\n"
            f"Name: {full_name}\n"
            f"Contact: {contact}\n"
            f"Property location: {property_location or '-'}\n"
            f"Service: {service or '-'}\n\n"
            f"Message:\n{requirement}\n",
        )
        flash("Thank you. Your enquiry has been received.", "success")
    return redirect(
        safe_next_url(request.form.get("next", ""))
        or url_for("index", _anchor="enquiry")
    )


app.register_blueprint(service_pages)


if __name__ == "__main__":
    app.run(debug=True)