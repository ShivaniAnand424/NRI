"""
properties.py
-------------
Flask Blueprint that adds:
  /properties                     listing with [All] [For Sale] [Sold] tabs
  /properties/<slug>              property detail (public info + locked info)
  /properties/<slug>/go/<action>  high-intent action -> login/register gate -> unlock
  /properties/<slug>/file/<name>  protected files (floor plan, brochure) - login required
  /client/register, /client/login, /client/logout
  /admin/leads?key=...            see which client registered for which property

Everything is stored in its own SQLite file (nri_clients.db), so it does not
touch your existing database.py.
"""
import os
import re
import secrets
import sqlite3
from urllib.parse import quote

from flask import (Blueprint, abort, current_app, flash, g, redirect,
                   render_template, render_template_string, request,
                   send_from_directory, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from property_data import PARTNER_LINE, PROPERTIES, WHATSAPP_NUMBER

bp = Blueprint("properties", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "nri_clients.db")
PRIVATE_DIR = os.path.join(BASE_DIR, "private_files")   # NOT inside /static, so it can't be guessed

BY_SLUG = {p["slug"]: p for p in PROPERTIES}

# The high-intent actions that require login / registration.
ACTIONS = {
    "price": "View Exact Price & Floor Plan",
    "details": "View Full Details / Video Walkthrough",
    "site_visit": "Schedule a Site Visit / Video Call",
    "enquire": "Enquire Now",
    "brochure": "Download Brochure",
}

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ----------------------------------------------------------------- database
def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                country TEXT,
                password_hash TEXT NOT NULL,
                signup_property TEXT,      -- property they were viewing when they registered
                signup_action TEXT,        -- the button they clicked
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS property_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                property_slug TEXT NOT NULL,
                action TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES clients(id)
            );
            """
        )


init_db()


def get_db():
    if "pm_db" not in g:
        g.pm_db = sqlite3.connect(DB_PATH)
        g.pm_db.row_factory = sqlite3.Row
    return g.pm_db


@bp.teardown_app_request
def close_db(_exc):
    db = g.pop("pm_db", None)
    if db is not None:
        db.close()


# ----------------------------------------------------------- session / csrf
def current_client():
    cid = session.get("client_id")
    if not cid:
        return None
    if "pm_client" not in g:
        g.pm_client = get_db().execute(
            "SELECT * FROM clients WHERE id = ?", (cid,)
        ).fetchone()
    return g.pm_client


def csrf_token():
    if "pm_csrf" not in session:
        session["pm_csrf"] = secrets.token_hex(16)
    return session["pm_csrf"]


def check_csrf():
    sent = request.form.get("pm_csrf", "")
    real = session.get("pm_csrf", "")
    if not sent or not real or not secrets.compare_digest(sent, real):
        abort(400, "Form expired. Please go back, refresh and try again.")


@bp.app_context_processor
def inject_helpers():
    # Available in EVERY template (including your navbar partial).
    return dict(current_client=current_client, pm_csrf=csrf_token)


# ------------------------------------------------------------------ helpers
def with_image(p):
    """Copy of the property with has_image=True only if the image file exists."""
    p = dict(p)
    img = p.get("image")
    p["has_image"] = bool(img) and os.path.exists(os.path.join(current_app.static_folder, img))
    return p


def private_file_exists(rel):
    return bool(rel) and os.path.isfile(os.path.join(PRIVATE_DIR, rel))


def log_lead(client_id, slug, action):
    db = get_db()
    db.execute(
        "INSERT INTO property_leads (client_id, property_slug, action) VALUES (?, ?, ?)",
        (client_id, slug, action),
    )
    db.commit()


def whatsapp_link(client, prop, action):
    text = (
        f"Hello, I'm {client['full_name']} ({client['email']}). "
        f"I'd like to {'schedule a site visit / video call for' if action == 'site_visit' else 'enquire about'} "
        f"{prop['name']}."
    )
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(text)}"


def clean_gate(form_or_args):
    """Validate the property/action carried through login & register forms."""
    slug = form_or_args.get("property", "")
    action = form_or_args.get("action", "")
    if slug not in BY_SLUG or action not in ACTIONS:
        return None, None
    return slug, action


# --------------------------------------------------------------- properties
@bp.route("/properties")
def listing():
    tab = request.args.get("tab", "all")
    if tab not in ("all", "sale", "sold"):
        tab = "all"
    props = [with_image(p) for p in PROPERTIES]
    props.sort(key=lambda p: p["status"] != "sale")        # for-sale first
    counts = {
        "all": len(props),
        "sale": sum(p["status"] == "sale" for p in props),
        "sold": sum(p["status"] == "sold" for p in props),
    }
    shown = [p for p in props if tab == "all" or p["status"] == tab]
    return render_template(
        "properties.html", properties=shown, tab=tab, counts=counts,
        partner_line=PARTNER_LINE, actions=ACTIONS,
    )


@bp.route("/properties/<slug>")
def detail(slug):
    prop = BY_SLUG.get(slug)
    if not prop:
        abort(404)
    prop = with_image(prop)
    client = current_client()
    files = []
    if client:                                   # files are only listed when logged in
        if private_file_exists(prop.get("layout_file")):
            files.append(("Floor / Layout Plan", "layout"))
        for i, (label, rel) in enumerate(prop.get("extra_files", [])):
            if private_file_exists(rel):
                files.append((label, f"extra-{i}"))
        if private_file_exists(prop.get("brochure_file")):
            files.append(("Brochure (PDF)", "brochure"))
    return render_template(
        "property_detail.html", p=prop, files=files, actions=ACTIONS,
        partner_line=PARTNER_LINE,
    )


@bp.route("/properties/<slug>/go/<action>")
def go(slug, action):
    """Every locked button points here."""
    prop = BY_SLUG.get(slug)
    if not prop or action not in ACTIONS:
        abort(404)
    client = current_client()
    if not client:
        # Not logged in -> send to register, remembering what they wanted.
        return redirect(url_for("properties.register", property=slug, action=action))

    log_lead(client["id"], slug, action)

    if action in ("enquire", "site_visit"):
        return redirect(whatsapp_link(client, prop, action))
    if action == "brochure":
        if private_file_exists(prop.get("brochure_file")):
            return redirect(url_for("properties.file", slug=slug, name="brochure"))
        flash("The brochure for this property is not uploaded yet. Please enquire and we will send it.", "info")
    return redirect(url_for("properties.detail", slug=slug) + "#unlocked")


@bp.route("/properties/<slug>/file/<name>")
def file(slug, name):
    prop = BY_SLUG.get(slug)
    if not prop:
        abort(404)
    if not current_client():
        return redirect(url_for("properties.register", property=slug, action="details"))
    rel = None
    if name == "layout":
        rel = prop.get("layout_file")
    elif name == "brochure":
        rel = prop.get("brochure_file")
    elif name.startswith("extra-") and name[6:].isdigit():
        extras = prop.get("extra_files", [])
        idx = int(name[6:])
        if idx < len(extras):
            rel = extras[idx][1]
    if not private_file_exists(rel):
        abort(404)
    return send_from_directory(PRIVATE_DIR, rel, as_attachment=(name == "brochure"))


# ------------------------------------------------------------- client auth
def gate_context(source):
    slug, action = clean_gate(source)
    return dict(
        gate_prop=BY_SLUG.get(slug) if slug else None,
        gate_slug=slug or "",
        gate_action=action or "",
        gate_action_label=ACTIONS.get(action, "") if action else "",
    )


def after_auth_redirect(slug, action):
    if slug and action:
        return redirect(url_for("properties.go", slug=slug, action=action))
    return redirect(url_for("properties.listing"))


@bp.route("/client/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        check_csrf()
        slug, action = clean_gate(request.form)
        name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        country = request.form.get("country", "").strip()
        password = request.form.get("password", "")

        error = None
        if len(name) < 2:
            error = "Please enter your full name."
        elif not EMAIL_RE.match(email):
            error = "Please enter a valid email address."
        elif len(re.sub(r"\D", "", phone)) < 7:
            error = "Please enter a valid phone / WhatsApp number with country code."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."

        if error:
            flash(error, "error")
        else:
            db = get_db()
            try:
                cur = db.execute(
                    """INSERT INTO clients
                       (full_name, email, phone, country, password_hash, signup_property, signup_action)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (name, email, phone, country, generate_password_hash(password), slug, action),
                )
                db.commit()
            except sqlite3.IntegrityError:
                flash("This email is already registered. Please log in.", "error")
                return redirect(url_for("properties.login", property=slug or "", action=action or ""))
            session.clear()
            session["client_id"] = cur.lastrowid
            flash(f"Welcome, {name.split()[0]}! Your account is ready.", "success")
            return after_auth_redirect(slug, action)

    source = request.form if request.method == "POST" else request.args
    return render_template("client_auth.html", mode="register", **gate_context(source))


@bp.route("/client/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        check_csrf()
        slug, action = clean_gate(request.form)
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        row = get_db().execute("SELECT * FROM clients WHERE email = ?", (email,)).fetchone()
        if row and check_password_hash(row["password_hash"], password):
            session.clear()
            session["client_id"] = row["id"]
            flash(f"Welcome back, {row['full_name'].split()[0]}!", "success")
            return after_auth_redirect(slug, action)
        flash("Incorrect email or password.", "error")

    source = request.form if request.method == "POST" else request.args
    return render_template("client_auth.html", mode="login", **gate_context(source))


@bp.route("/client/logout", methods=["POST"])
def logout():
    check_csrf()
    session.pop("client_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("properties.listing"))


# -------------------------------------------------------------- admin leads
ADMIN_TEMPLATE = """
<!doctype html><meta charset="utf-8"><title>Leads</title>
<style>body{font:14px system-ui;margin:24px}table{border-collapse:collapse;margin-bottom:32px}
td,th{border:1px solid #ccc;padding:6px 10px;text-align:left}th{background:#f2f2f2}</style>
<h2>Registered clients (tagged with the property they were viewing)</h2>
<table><tr><th>Date</th><th>Name</th><th>Email</th><th>Phone</th><th>Country</th>
<th>Signed up on property</th><th>Via button</th></tr>
{% for c in clients %}<tr><td>{{c.created_at}}</td><td>{{c.full_name}}</td><td>{{c.email}}</td>
<td>{{c.phone}}</td><td>{{c.country}}</td><td>{{c.signup_property or '-'}}</td>
<td>{{c.signup_action or '-'}}</td></tr>{% endfor %}</table>
<h2>Every high-intent click</h2>
<table><tr><th>Date</th><th>Name</th><th>Phone</th><th>Property</th><th>Action</th></tr>
{% for l in leads %}<tr><td>{{l.created_at}}</td><td>{{l.full_name}}</td><td>{{l.phone}}</td>
<td>{{l.property_slug}}</td><td>{{l.action}}</td></tr>{% endfor %}</table>
"""


@bp.route("/admin/leads")
def admin_leads():
    key = os.environ.get("NRI_ADMIN_KEY", "")
    if not key or not secrets.compare_digest(request.args.get("key", ""), key):
        abort(404)
    db = get_db()
    clients = db.execute("SELECT * FROM clients ORDER BY id DESC LIMIT 500").fetchall()
    leads = db.execute(
        """SELECT l.created_at, l.property_slug, l.action, c.full_name, c.phone
           FROM property_leads l JOIN clients c ON c.id = l.client_id
           ORDER BY l.id DESC LIMIT 500"""
    ).fetchall()
    return render_template_string(ADMIN_TEMPLATE, clients=clients, leads=leads)
