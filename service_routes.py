import json
import sqlite3
from contextlib import closing

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from csrf import validate_csrf
from service_catalog import COMMON_FIELDS, get_service_page


service_pages = Blueprint("service_pages", __name__)


@service_pages.route("/services/<slug>", methods=["GET", "POST"])
def service_detail(slug):
    service = get_service_page(slug)
    if service is None:
        abort(404)

    if session.get("user_id") is None:
        return redirect(url_for("login", next=request.path))

    if request.method == "POST":
        validate_csrf()
        fields = COMMON_FIELDS + service["fields"]
        responses = {}
        invalid = False

        for field in fields:
            name = field["name"]
            if field["type"] == "checkboxes":
                value = request.form.getlist(name)
            else:
                value = request.form.get(name, "").strip()

            if field["required"] and not value:
                invalid = True

            options = field.get("options")
            selected = value if isinstance(value, list) else [value]
            if options and any(item and item not in options for item in selected):
                invalid = True

            responses[name] = value

        if invalid:
            flash("Please complete the required fields with valid options.", "error")
            return render_template(
                "service_detail.html",
                service=service,
                common_fields=COMMON_FIELDS,
                service_slug=slug,
                form_data=request.form,
            ), 400

        with closing(sqlite3.connect(current_app.config["DATABASE"])) as db, db:
            db.execute(
                """
                INSERT INTO service_enquiries (user_id, service_slug, responses_json)
                VALUES (?, ?, ?)
                """,
                (
                    session["user_id"],
                    slug,
                    json.dumps(responses),
                ),
            )

        flash("Your service enquiry has been submitted.", "success")
        return redirect(url_for("service_pages.service_detail", slug=slug))

    return render_template(
        "service_detail.html",
        service=service,
        common_fields=COMMON_FIELDS,
        service_slug=slug,
        form_data=request.form,
    )