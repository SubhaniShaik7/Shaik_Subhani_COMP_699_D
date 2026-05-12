from core.db_extensions import db
from core.domain.task_entity import Task
from datetime import datetime


# -----------------------------
# ADD CUSTOM TASK (9)
# -----------------------------
def add_custom_task(plan_id, title, category):
    try:
        if not plan_id or not title:
            return None

        task = Task(
            plan_id=plan_id,
            title=title.strip(),
            category=category.strip() if category else "custom",
            status="pending",
            priority="medium"
        )

        db.session.add(task)
        db.session.commit()

        return task

    except Exception:
        db.session.rollback()
        return None


# -----------------------------
# EDIT TASK (10)
# -----------------------------
def edit_task(task_id, title=None, category=None):
    try:
        task = Task.query.get(task_id)
        if not task:
            return False

        if title:
            title = title.strip()

        if category:
            category = category.strip()

        task.update_task(title=title, category=category)

        db.session.commit()
        return True

    except Exception:
        db.session.rollback()
        return False


# -----------------------------
# DELETE TASK (11)
# -----------------------------
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return False

        db.session.delete(task)
        db.session.commit()

        return True

    except Exception:
        db.session.rollback()
        return False


# -----------------------------
# MARK TASK COMPLETE (12)
# -----------------------------
def complete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return False

        task.mark_completed()
        db.session.commit()

        return True

    except Exception:
        db.session.rollback()
        return False


# -----------------------------
# SET DUE DATE (13)
# -----------------------------
def assign_due_date(task_id, due_date_str):
    try:
        task = Task.query.get(task_id)
        if not task or not due_date_str:
            return False

        due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")

        task.set_due_date(due_date)
        db.session.commit()

        return True

    except Exception:
        db.session.rollback()
        return False


# -----------------------------
# SET PRIORITY (14)
# -----------------------------
def set_task_priority(task_id, priority):
    try:
        task = Task.query.get(task_id)
        if not task:
            return False

        if priority not in ["low", "medium", "high"]:
            return False

        task.set_priority(priority)
        db.session.commit()

        return True

    except Exception:
        db.session.rollback()
        return False