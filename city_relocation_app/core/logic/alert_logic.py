from core.db_extensions import db
from core.domain.task_entity import Task
from core.domain.reminder_entity import Reminder
from datetime import datetime, timedelta


# -----------------------------
# CREATE REMINDER FOR TASK
# -----------------------------
def create_reminder(task_id):
    try:
        task = Task.query.get(task_id)

        if not task or not task.due_date:
            return None

        # prevent duplicate reminders
        existing = Reminder.query.filter_by(task_id=task.id).first()
        if existing:
            return existing

        trigger_time = task.due_date - timedelta(hours=1)

        reminder = Reminder(
            task_id=task.id,
            trigger_time=trigger_time,
            sent=False
        )

        db.session.add(reminder)
        db.session.commit()

        return reminder

    except Exception:
        db.session.rollback()
        return None


# -----------------------------
# CHECK AND TRIGGER REMINDERS (15,16)
# -----------------------------
def process_reminders():
    try:
        now = datetime.utcnow()

        reminders = Reminder.query.filter(
            Reminder.sent == False,
            Reminder.trigger_time <= now
        ).all()

        for reminder in reminders:
            try:
                reminder.send()
            except Exception:
                continue  # skip broken reminder

        db.session.commit()

    except Exception:
        db.session.rollback()


# -----------------------------
# AUTO GENERATE REMINDERS FOR TASKS
# -----------------------------
def generate_task_reminders():
    try:
        tasks = Task.query.filter(Task.due_date != None).all()

        for task in tasks:
            existing = Reminder.query.filter_by(task_id=task.id).first()

            if not existing:
                create_reminder(task.id)

    except Exception:
        db.session.rollback()


# -----------------------------
# PRIORITY BASED ALERT CHECK
# -----------------------------
def check_priority_alerts():
    try:
        tasks = Task.query.filter_by(status="pending").all()

        now = datetime.utcnow()

        for task in tasks:
            try:
                if task.due_date and (task.due_date - now).total_seconds() <= 3600:
                    # within 1 hour
                    print(f"Priority Alert: Task '{task.title}' is due soon")
            except Exception:
                continue

    except Exception:
        pass