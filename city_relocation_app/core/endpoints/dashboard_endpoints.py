from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# -----------------------------
# VIEW DASHBOARD
# -----------------------------
@dashboard_bp.route("/")
@login_required
def view_dashboard():
    try:
        # ✅ SAFE FIX (MAIN CHANGE)
        # always get or create planner
        planner = current_user.get_planner()

    except Exception as e:
        print("PLANNER ERROR:", str(e))
        flash("System error while loading your profile.", "error")

        return render_template(
            "dashboard_view.html",
            data=None,
            plans=[],
            is_empty=True
        )

    # -----------------------------
    # DASHBOARD DATA
    # -----------------------------
    try:
        dashboard_data = planner.view_dashboard()
    except Exception as e:
        print("DASHBOARD ERROR:", str(e))
        dashboard_data = None
        flash("Unable to load dashboard data.", "error")

    # -----------------------------
    # PLANS LIST
    # -----------------------------
    try:
        plans = sorted(
            planner.plans,
            key=lambda p: p.id,
            reverse=True
        )
    except Exception as e:
        print("PLAN LOAD ERROR:", str(e))
        plans = []

    # -----------------------------
    # FINAL RENDER
    # -----------------------------
    return render_template(
        "dashboard_view.html",
        data=dashboard_data,
        plans=plans,
        is_empty=(len(plans) == 0)
    )