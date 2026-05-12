from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from core.logic.city_logic import get_city_services
from core.logic.authentication_logic import accept_privacy
from core.helpers.common_utils import to_int

misc_bp = Blueprint("misc", __name__, url_prefix="/misc")


# -----------------------------
# VIEW SERVICES (17,18)
# -----------------------------
@misc_bp.route("/services/<int:city_id>")
@login_required
def services(city_id):
    city_id = to_int(city_id)

    # ❗ real error → use flash
    if not city_id:
        flash("Invalid city selected", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    try:
        services_list = get_city_services(city_id)
    except Exception as e:
        print("SERVICES ERROR:", str(e))
        flash("Unable to load services", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    # ❌ DO NOT FLASH EMPTY DATA
    # if not services_list:
    #     flash("No services found")

    # ✔ pass flag to UI instead
    return render_template(
        "services_view.html",
        services=services_list,
        is_empty=(len(services_list) == 0)
    )


# -----------------------------
# PRIVACY PAGE (24)
# -----------------------------
@misc_bp.route("/privacy")
def privacy():
    return render_template("privacy.html")


# -----------------------------
# ACCEPT PRIVACY (25)
# -----------------------------
@misc_bp.route("/accept_privacy")
@login_required
def accept_privacy_route():
    try:
        result = accept_privacy(current_user.id)

        if result:
            flash("Privacy policy accepted", "success")
        else:
            flash("Operation failed", "error")

    except Exception as e:
        print("PRIVACY ERROR:", str(e))
        flash("Something went wrong", "error")

    return redirect(url_for("dashboard.view_dashboard"))