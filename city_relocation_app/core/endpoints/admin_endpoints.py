from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required
from core.logic.admin_logic import (
    create_city,
    add_template,
    update_template,
    load_housing_data,
    load_utility_data,
    load_document_data,
    load_service,
    refresh_all_data,

    # planner functions
    create_planner_for_user,
    delete_planner,
    assign_planner
)
from core.helpers.security_utils import admin_required, sanitize_input
from core.helpers.common_utils import to_int

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# =====================================================
# ✅ ADMIN PANEL PAGE (THIS WAS MISSING - MAIN FIX)
# =====================================================
@admin_bp.route("/panel")
@login_required
@admin_required
def admin_panel():
    return render_template("admin_panel.html")


# -----------------------------
# CREATE CITY
# -----------------------------
@admin_bp.route("/create_city", methods=["POST"])
@login_required
@admin_required
def create_city_route():
    name = sanitize_input(request.form.get("name"))
    state = sanitize_input(request.form.get("state"))
    country = sanitize_input(request.form.get("country"))

    if not name:
        flash("City name required", "error")
        return redirect(url_for("admin.admin_panel"))

    result = create_city(name, state, country)

    flash("City created successfully" if result else "Failed to create city",
          "success" if result else "error")

    return redirect(url_for("admin.admin_panel"))


# -----------------------------
# ADD TEMPLATE
# -----------------------------
@admin_bp.route("/add_template", methods=["POST"])
@login_required
@admin_required
def add_template_route():
    city_id = to_int(request.form.get("city_id"))
    category = sanitize_input(request.form.get("category"))
    title = sanitize_input(request.form.get("title"))

    if not city_id or not title:
        flash("Invalid template data", "error")
        return redirect(url_for("admin.admin_panel"))

    result = add_template(city_id, category, title)

    flash("Template added successfully" if result else "Failed to add template",
          "success" if result else "error")

    return redirect(url_for("admin.admin_panel"))


# -----------------------------
# UPDATE TEMPLATE
# -----------------------------
@admin_bp.route("/update_template", methods=["POST"])
@login_required
@admin_required
def update_template_route():
    template_id = to_int(request.form.get("template_id"))
    title = sanitize_input(request.form.get("title"))
    category = sanitize_input(request.form.get("category"))

    if not template_id:
        flash("Invalid template id", "error")
        return redirect(url_for("admin.admin_panel"))

    result = update_template(template_id, new_title=title, new_category=category)

    flash("Template updated" if result else "Update failed",
          "success" if result else "error")

    return redirect(url_for("admin.admin_panel"))


# -----------------------------
# LOAD SERVICE LIST
# -----------------------------
@admin_bp.route("/load_service", methods=["POST"])
@login_required
@admin_required
def load_service_route():
    city_id = to_int(request.form.get("city_id"))
    name = sanitize_input(request.form.get("name"))
    address = sanitize_input(request.form.get("address"))
    service_type = sanitize_input(request.form.get("type"))

    if not city_id or not name or not service_type:
        flash("Invalid service data", "error")
        return redirect(url_for("admin.admin_panel"))

    result = load_service(city_id, name, address, service_type)

    flash("Service added successfully" if result else "Failed to add service",
          "success" if result else "error")

    return redirect(url_for("admin.admin_panel"))


# -----------------------------
# REFRESH DATASETS
# -----------------------------
@admin_bp.route("/refresh_data")
@login_required
@admin_required
def refresh_data():
    result = refresh_all_data()

    flash("System data refreshed" if result else "Refresh failed",
          "success" if result else "error")

    return redirect(url_for("admin.admin_panel"))


# =====================================================
# 🆕 PLANNER MANAGEMENT
# =====================================================

@admin_bp.route("/create_planner", methods=["POST"])
@login_required
@admin_required
def create_planner():
    user_id = to_int(request.form.get("user_id"))

    if not user_id:
        flash("Invalid user id", "error")
        return redirect(url_for("admin.admin_panel"))

    result = create_planner_for_user(user_id)

    flash("Planner created successfully" if result else "Failed",
          "success" if result else "error")

    return redirect(url_for("admin.admin_panel"))


@admin_bp.route("/delete_planner", methods=["POST"])
@login_required
@admin_required
def delete_planner_route():
    user_id = to_int(request.form.get("user_id"))

    if not user_id:
        flash("Invalid user id", "error")
        return redirect(url_for("admin.admin_panel"))

    result = delete_planner(user_id)

    flash("Planner deleted" if result else "Failed",
          "success" if result else "error")

    return redirect(url_for("admin.admin_panel"))


@admin_bp.route("/assign_planner", methods=["POST"])
@login_required
@admin_required
def assign_planner_route():
    user_id = to_int(request.form.get("user_id"))

    if not user_id:
        flash("Invalid user id", "error")
        return redirect(url_for("admin.admin_panel"))

    result = assign_planner(user_id)

    flash("Planner assigned" if result else "Failed",
          "success" if result else "error")

    return redirect(url_for("admin.admin_panel"))