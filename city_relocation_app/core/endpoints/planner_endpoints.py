from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core.logic.relocation_logic import (
    create_relocation_plan,
    get_available_cities,
    generate_checklist,
    clear_completed_tasks
)
from core.domain.relocation_entity import RelocationPlan
from core.helpers.common_utils import to_int
from core.helpers.security_utils import sanitize_input

planner_bp = Blueprint("planner", __name__, url_prefix="/planner")


# -----------------------------
# CREATE RELOCATION PLAN
# -----------------------------
@planner_bp.route("/create_plan", methods=["GET", "POST"])
@login_required
def create_plan():
    try:
        # ✅ FIX: always get planner safely
        planner = current_user.get_planner()
    except Exception as e:
        print("PLANNER ERROR:", str(e))
        flash("Unable to load planner profile", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    # -----------------------------
    # POST → CREATE PLAN
    # -----------------------------
    if request.method == "POST":
        city_id = to_int(request.form.get("city_id"))

        if not city_id:
            flash("Please select a valid city", "error")
            return redirect(url_for("planner.create_plan"))

        try:
            plan = create_relocation_plan(planner.id, city_id)

            if not plan:
                flash("Failed to create plan", "error")
            else:
                flash("Relocation plan created successfully", "success")

        except Exception as e:
            print("CREATE PLAN ERROR:", str(e))
            flash("Something went wrong while creating the plan", "error")

        return redirect(url_for("dashboard.view_dashboard"))

    # -----------------------------
    # GET → LOAD FORM
    # -----------------------------
    try:
        cities = get_available_cities()
    except Exception as e:
        print("CITY LOAD ERROR:", str(e))
        cities = []
        flash("Unable to load cities", "error")

    return render_template(
        "relocation_view.html",
        cities=cities,
        is_empty=(len(cities) == 0)
    )


# -----------------------------
# UPDATE ALERT PREFERENCE
# -----------------------------
@planner_bp.route("/update_alert", methods=["POST"])
@login_required
def update_alert():
    preference = sanitize_input(request.form.get("preference"))

    if not preference:
        flash("Invalid preference", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    try:
        # ✅ FIX
        planner = current_user.get_planner()
    except Exception as e:
        print("PLANNER ERROR:", str(e))
        flash("Planner not found", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    try:
        planner.update_alert_preference(preference)
        flash("Alert preference updated", "success")
    except Exception as e:
        print("ALERT UPDATE ERROR:", str(e))
        flash("Failed to update alert preference", "error")

    return redirect(url_for("dashboard.view_dashboard"))


# -----------------------------
# DOWNLOAD CHECKLIST
# -----------------------------
@planner_bp.route("/checklist/<int:plan_id>")
@login_required
def checklist(plan_id):
    plan = RelocationPlan.query.get(plan_id)

    # 🔐 SECURITY CHECK
    if not plan or plan.planner.user_id != current_user.id:
        return "Unauthorized", 403

    try:
        checklist_data = generate_checklist(plan_id)
    except Exception as e:
        print("CHECKLIST ERROR:", str(e))
        flash("Unable to generate checklist", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    return render_template(
        "export_checklist.html",
        checklist=checklist_data
    )


# -----------------------------
# CLEAR COMPLETED TASKS
# -----------------------------
@planner_bp.route("/clear_completed/<int:plan_id>")
@login_required
def clear_completed(plan_id):
    plan = RelocationPlan.query.get(plan_id)

    # 🔐 SECURITY CHECK
    if not plan or plan.planner.user_id != current_user.id:
        return "Unauthorized", 403

    try:
        success = clear_completed_tasks(plan_id)

        if success:
            flash("Completed tasks cleared", "success")
        else:
            flash("No completed tasks to clear", "info")

    except Exception as e:
        print("CLEAR TASK ERROR:", str(e))
        flash("Failed to clear tasks", "error")

    return redirect(url_for("dashboard.view_dashboard"))