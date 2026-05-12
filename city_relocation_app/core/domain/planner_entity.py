from core.db_extensions import db
from datetime import datetime


class RelocationPlanner(db.Model):
    __tablename__ = "relocation_planners"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True  # one user = one planner
    )

    alert_preference = db.Column(db.String(50), default="in_app")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -----------------------------
    # RELATIONSHIPS
    # -----------------------------
    user = db.relationship(
        "User",
        back_populates="planner",
        lazy="joined"
    )

    plans = db.relationship(
        "RelocationPlan",
        back_populates="planner",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # -----------------------------
    # SAFE GETTER (IMPORTANT FIX)
    # -----------------------------
    @staticmethod
    def get_or_create_planner(user_id):
        planner = RelocationPlanner.query.filter_by(user_id=user_id).first()

        if not planner:
            planner = RelocationPlanner(user_id=user_id)
            db.session.add(planner)
            db.session.commit()

        return planner

    # -----------------------------
    # TASK VIEWS
    # -----------------------------
    def view_tasks(self):
        return [task for plan in self.plans for task in plan.tasks]

    def view_tasks_by_category(self, category):
        return [
            task
            for plan in self.plans
            for task in plan.tasks
            if task.category == category
        ]

    def get_pending_tasks(self):
        return [
            task
            for plan in self.plans
            for task in plan.tasks
            if task.status == "pending"
        ]

    def get_completed_tasks(self):
        return [
            task
            for plan in self.plans
            for task in plan.tasks
            if task.status == "completed"
        ]

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    def view_dashboard(self):
        tasks = self.view_tasks()

        total = len(tasks)
        completed = sum(1 for t in tasks if t.status == "completed")

        progress = (completed / total) * 100 if total > 0 else 0

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": total - completed,
            "progress": int(progress)
        }

    # -----------------------------
    # CHECKLIST EXPORT
    # -----------------------------
    def download_checklist(self):
        return [
            {
                "title": task.title,
                "status": task.status,
                "due_date": task.due_date
            }
            for plan in self.plans
            for task in plan.tasks
        ]

    # -----------------------------
    # CLEAR COMPLETED TASKS
    # -----------------------------
    def clear_completed_tasks(self):
        for plan in self.plans:
            for task in plan.tasks:
                if task.status == "completed":
                    db.session.delete(task)

    # -----------------------------
    # ALERT SETTINGS
    # -----------------------------
    def update_alert_preference(self, preference):
        if preference in ["in_app", "email", "none"]:
            self.alert_preference = preference
            db.session.commit()

    # -----------------------------
    # ADMIN SUPPORT (NEW)
    # -----------------------------
    @staticmethod
    def create_for_user(user_id):
        existing = RelocationPlanner.query.filter_by(user_id=user_id).first()
        if existing:
            return existing

        planner = RelocationPlanner(user_id=user_id)
        db.session.add(planner)
        db.session.commit()
        return planner

    @staticmethod
    def delete_for_user(user_id):
        planner = RelocationPlanner.query.filter_by(user_id=user_id).first()
        if planner:
            db.session.delete(planner)
            db.session.commit()

    # -----------------------------
    # STRING REPRESENTATION
    # -----------------------------
    def __repr__(self):
        return f"<RelocationPlanner id={self.id}, user_id={self.user_id}>"