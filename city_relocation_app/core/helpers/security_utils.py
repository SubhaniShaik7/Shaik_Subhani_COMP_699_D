from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
import re


# -----------------------------
# ADMIN ACCESS DECORATOR
# -----------------------------
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please login first", "error")
            return redirect(url_for("auth.home"))

        if current_user.role != "admin":
            flash("Admin access required", "error")
            return redirect(url_for("dashboard.view_dashboard"))

        return func(*args, **kwargs)

    return wrapper


# -----------------------------
# INPUT SANITIZATION
# -----------------------------
def sanitize_input(value):
    if not value:
        return ""

    value = value.strip()

    # remove dangerous characters
    value = re.sub(r"[<>\"']", "", value)

    return value


# -----------------------------
# PASSWORD VALIDATION
# -----------------------------
def validate_password(password):
    if not password:
        return False

    password = password.strip()

    # minimum 6 chars + at least one digit
    if len(password) < 6:
        return False

    if not any(char.isdigit() for char in password):
        return False

    return True


# -----------------------------
# ROLE CHECK HELPERS
# -----------------------------
def is_admin_user():
    return current_user.is_authenticated and current_user.role == "admin"


def is_authenticated_user():
    return current_user.is_authenticated