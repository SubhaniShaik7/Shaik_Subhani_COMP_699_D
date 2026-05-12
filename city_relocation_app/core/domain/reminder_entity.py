from core.db_extensions import db
from datetime import datetime


class Reminder(db.Model):
    __tablename__ = "reminders"

    id = db.Column(db.Integer, primary_key=True)

    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id"),
        nullable=False
    )

    trigger_time = db.Column(db.DateTime, nullable=False)

    sent = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -----------------------------
    # SET SCHEDULE
    # -----------------------------
    def schedule(self, trigger_time):
        if isinstance(trigger_time, datetime):
            self.trigger_time = trigger_time

    # -----------------------------
    # SEND REMINDER (15,16)
    # -----------------------------
    def send(self):
        if not self.sent:
            print(f"Reminder: Task '{self.task.title}' is due soon.")
            self.sent = True  # commit handled in logic layer

    # -----------------------------
    # CHECK TRIGGER CONDITION
    # -----------------------------
    def should_trigger(self):
        if self.sent or not self.trigger_time:
            return False

        return datetime.utcnow() >= self.trigger_time

    # -----------------------------
    # STRING REPRESENTATION
    # -----------------------------
    def __repr__(self):
        return f"<Reminder task_id={self.task_id} sent={self.sent}>"