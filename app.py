import os
import secrets
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    send_from_directory,
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
from property_data import PARTNER_LINE, PROPERTIES as PROPERTY_LISTINGS
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
PRIVATE_FILES_DIR = Path(app.root_path) / "private_files"

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


PROPERTY_BY_SLUG = {item["slug"]: item for item in PROPERTY_LISTINGS}


def _property_for_display(item):
    property_item = dict(item)
    image_path = Path(app.static_folder) / item["image"]
    property_item["has_image"] = image_path.is_file()
    return property_item


def _private_property_file_exists(relative_path):
    return bool(relative_path) and (PRIVATE_FILES_DIR / relative_path).is_file()


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


@app.route("/properties/sold")
def sold_properties():
    properties = [
        _property_for_display(item)
        for item in PROPERTY_LISTINGS
        if item["status"] == "sold"
    ]
    return render_template(
        "properties.html",
        properties=properties,
        property_status="sold",
        page_title="Sold Properties | NRIPMC",
        partner_line=PARTNER_LINE,
    )


@app.route("/properties/ongoing")
def ongoing_properties():
    properties = [
        _property_for_display(item)
        for item in PROPERTY_LISTINGS
        if item["status"] in ("sale", "ongoing")
    ]
    return render_template(
        "properties.html",
        properties=properties,
        property_status="ongoing",
        page_title="Ongoing Properties | NRIPMC",
        partner_line=PARTNER_LINE,
    )


@app.route("/properties/<slug>")
def property_detail(slug):
    property_item = PROPERTY_BY_SLUG.get(slug)
    if property_item is None:
        abort(404)

    property_item = _property_for_display(property_item)
    documents = []
    if session.get("user_id") is not None:
        if _private_property_file_exists(property_item.get("layout_file")):
            documents.append(("Floor / Layout Plan", "layout"))
        for index, (label, relative_path) in enumerate(
            property_item.get("extra_files", [])
        ):
            if _private_property_file_exists(relative_path):
                documents.append((label, f"extra-{index}"))

    return render_template(
        "property_detail.html",
        property=property_item,
        documents=documents,
        partner_line=PARTNER_LINE,
        page_title=f"{property_item['name']} | NRIPMC",
    )


@app.route("/properties/<slug>/file/<name>")
def property_file(slug, name):
    property_item = PROPERTY_BY_SLUG.get(slug)
    if property_item is None:
        abort(404)
    user_id = session.get("user_id")
    user_exists = user_id is not None and get_db().execute(
        text("SELECT 1 FROM users WHERE id = :user_id"),
        {"user_id": user_id},
    ).first()
    if not user_exists:
        session.clear()
        flash("Please log in to view this property document.", "error")
        return redirect(url_for("login", next=request.path))

    if name == "layout":
        relative_path = property_item.get("layout_file")
    elif name.startswith("extra-") and name[6:].isdigit():
        extra_files = property_item.get("extra_files", [])
        index = int(name[6:])
        relative_path = extra_files[index][1] if index < len(extra_files) else None
    else:
        relative_path = None

    if not _private_property_file_exists(relative_path):
        abort(404)
    return send_from_directory(PRIVATE_FILES_DIR, relative_path)


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