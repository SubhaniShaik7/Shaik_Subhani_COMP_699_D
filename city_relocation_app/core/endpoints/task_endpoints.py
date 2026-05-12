from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core.logic.task_logic import (
    add_custom_task,
    edit_task,
    delete_task,
    complete_task,
    assign_due_date,
    set_task_priority
)
from core.domain.task_entity import Task
from core.helpers.common_utils import to_int
from core.helpers.security_utils import sanitize_input

task_bp = Blueprint("task", __name__, url_prefix="/task")


# -----------------------------
# HELPER: CHECK TASK OWNERSHIP
# -----------------------------
def is_task_owner(task):
    return task and task.plan and task.plan.planner.user_id == current_user.id


# -----------------------------
# ADD CUSTOM TASK (9)
# -----------------------------
@task_bp.route("/add", methods=["POST"])
@login_required
def add():
    plan_id = to_int(request.form.get("plan_id"))
    title = sanitize_input(request.form.get("title"))
    category = sanitize_input(request.form.get("category"))

    if not plan_id or not title:
        flash("Invalid task data", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    task = add_custom_task(plan_id, title, category)

    if task:
        flash("Task added successfully", "success")
    else:
        flash("Failed to add task", "error")

    return redirect(url_for("dashboard.view_dashboard"))


# -----------------------------
# EDIT TASK (10)
# -----------------------------
@task_bp.route("/edit/<int:task_id>", methods=["POST"])
@login_required
def edit(task_id):
    task = Task.query.get(task_id)

    if not is_task_owner(task):
        return "Unauthorized", 403

    title = sanitize_input(request.form.get("title"))
    category = sanitize_input(request.form.get("category"))

    updated = edit_task(task_id, title=title, category=category)

    if updated:
        flash("Task updated successfully", "success")
    else:
        flash("Update failed", "error")

    return redirect(url_for("dashboard.view_dashboard"))


# -----------------------------
# DELETE TASK (11)
# -----------------------------
@task_bp.route("/delete/<int:task_id>")
@login_required
def delete(task_id):
    task = Task.query.get(task_id)

    if not is_task_owner(task):
        return "Unauthorized", 403

    success = delete_task(task_id)

    if success:
        flash("Task deleted", "success")
    else:
        flash("Delete failed", "error")

    return redirect(url_for("dashboard.view_dashboard"))


# -----------------------------
# MARK COMPLETE (12)
# -----------------------------
@task_bp.route("/complete/<int:task_id>")
@login_required
def complete(task_id):
    task = Task.query.get(task_id)

    if not is_task_owner(task):
        return "Unauthorized", 403

    result = complete_task(task_id)

    if result:
        flash("Task marked as completed", "success")
    else:
        flash("Operation failed", "error")

    return redirect(url_for("dashboard.view_dashboard"))


# -----------------------------
# SET DUE DATE (13)
# -----------------------------
@task_bp.route("/due/<int:task_id>", methods=["POST"])
@login_required
def due(task_id):
    task = Task.query.get(task_id)

    if not is_task_owner(task):
        return "Unauthorized", 403

    due_date = request.form.get("due_date")

    if not due_date:
        flash("Invalid date", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    result = assign_due_date(task_id, due_date)

    if result:
        flash("Due date updated", "success")
    else:
        flash("Invalid date format", "error")

    return redirect(url_for("dashboard.view_dashboard"))


# -----------------------------
# SET PRIORITY (14)
# -----------------------------
@task_bp.route("/priority/<int:task_id>", methods=["POST"])
@login_required
def priority(task_id):
    task = Task.query.get(task_id)

    if not is_task_owner(task):
        return "Unauthorized", 403

    priority = sanitize_input(request.form.get("priority"))

    if priority not in ["low", "medium", "high"]:
        flash("Invalid priority", "error")
        return redirect(url_for("dashboard.view_dashboard"))

    result = set_task_priority(task_id, priority)

    if result:
        flash("Priority updated", "success")
    else:
        flash("Update failed", "error")

    return redirect(url_for("dashboard.view_dashboard"))