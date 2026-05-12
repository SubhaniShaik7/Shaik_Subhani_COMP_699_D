from core.db_extensions import db
from datetime import datetime


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    plan_id = db.Column(
        db.Integer,
        db.ForeignKey("relocation_plans.id"),
        nullable=False
    )

    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50))  # housing, documents, utilities, services, custom

    status = db.Column(db.String(50), default="pending")

    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), default="medium")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # -----------------------------
    # 🔥 FIXED RELATIONSHIP (IMPORTANT)
    # -----------------------------
    plan = db.relationship(
        "RelocationPlan",
        back_populates="tasks"
    )

    # one task -> many reminders
    reminders = db.relationship(
        "Reminder",
        backref="task",
        cascade="all, delete-orphan",
        lazy=True
    )

    # -----------------------------
    # MARK COMPLETED (12)
    # -----------------------------
    def mark_completed(self):
        self.status = "completed"

    # -----------------------------
    # SET DUE DATE (13)
    # -----------------------------
    def set_due_date(self, due_date):
        if isinstance(due_date, datetime):
            self.due_date = due_date

    # -----------------------------
    # SET PRIORITY (14)
    # -----------------------------
    def set_priority(self, priority):
        if priority in ["low", "medium", "high"]:
            self.priority = priority

    # -----------------------------
    # EDIT TASK (10)
    # -----------------------------
    def update_task(self, title=None, category=None):
        if title:
            self.title = title.strip()

        if category:
            self.category = category.strip()

    # -----------------------------
    # DELETE TASK (11)
    # -----------------------------
    def delete_task(self):
        db.session.delete(self)

    # -----------------------------
    # HELPER: CHECK IF DUE SOON
    # -----------------------------
    def is_due_soon(self):
        if not self.due_date:
            return False

        now = datetime.utcnow()
        diff = (self.due_date - now).total_seconds()

        return diff <= 3600 or self.priority == "high"

    # -----------------------------
    # STRING REPRESENTATION
    # -----------------------------
    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"