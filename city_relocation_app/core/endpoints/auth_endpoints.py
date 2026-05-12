from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core.logic.authentication_logic import (
    register_user,
    login_account,
    logout_account,
    update_profile,
    accept_privacy
)
from core.helpers.security_utils import sanitize_input, validate_password

auth_bp = Blueprint("auth", __name__)


# -----------------------------
# HOME / LOGIN PAGE
# -----------------------------
@auth_bp.route("/", methods=["GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.view_dashboard"))

    return render_template("signin.html")


# -----------------------------
# REGISTER USER
# -----------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.view_dashboard"))

    if request.method == "POST":
        name = sanitize_input(request.form.get("name"))
        email = sanitize_input(request.form.get("email"))
        password = request.form.get("password")

        # validation
        if not name or not email or not password:
            flash("All fields are required", "error")
            return redirect(url_for("auth.register"))

        if not validate_password(password):
            flash("Password must be at least 6 characters", "error")
            return redirect(url_for("auth.register"))

        # 🔥 FIXED LOGIC HANDLING
        result = register_user(name, email, password)

        if result == "exists":
            flash("User already exists", "error")
            return redirect(url_for("auth.register"))

        elif result == "error":
            flash("Something went wrong. Check server logs.", "error")
            return redirect(url_for("auth.register"))

        else:
            flash("Registration successful. Please login.", "success")
            return redirect(url_for("auth.home"))

    return render_template("signup.html")


# -----------------------------
# LOGIN USER
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.view_dashboard"))

    email = sanitize_input(request.form.get("email"))
    password = request.form.get("password")

    if not email or not password:
        flash("Email and password required", "error")
        return redirect(url_for("auth.home"))

    user = login_account(email, password)

    if user:
        flash("Login successful", "success")
        return redirect(url_for("dashboard.view_dashboard"))

    flash("Invalid credentials", "error")
    return redirect(url_for("auth.home"))


# -----------------------------
# LOGOUT USER
# -----------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_account()
    flash("Logged out successfully", "success")
    return redirect(url_for("auth.home"))


# -----------------------------
# UPDATE PROFILE
# -----------------------------
@auth_bp.route("/update_profile", methods=["POST"])
@login_required
def update_user_profile():
    new_name = sanitize_input(request.form.get("name"))

    if not new_name:
        flash("Name cannot be empty", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    update_profile(current_user.id, new_name)

    flash("Profile updated successfully", "success")
    return redirect(url_for("dashboard.view_dashboard"))


# -----------------------------
# ACCEPT PRIVACY
# -----------------------------
@auth_bp.route("/accept_privacy")
@login_required
def accept_privacy_route():
    accept_privacy(current_user.id)

    flash("Privacy policy accepted", "success")
    return redirect(url_for("dashboard.view_dashboard"))