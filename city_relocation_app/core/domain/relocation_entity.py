from core.db_extensions import db
from datetime import datetime


class RelocationPlan(db.Model):
    __tablename__ = "relocation_plans"

    id = db.Column(db.Integer, primary_key=True)

    planner_id = db.Column(
        db.Integer,
        db.ForeignKey("relocation_planners.id", ondelete="CASCADE"),
        nullable=False
    )

    city_id = db.Column(
        db.Integer,
        db.ForeignKey("cities.id", ondelete="CASCADE"),
        nullable=False
    )

    status = db.Column(db.String(50), default="in_progress")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -----------------------------
    # RELATIONSHIPS (STRICT MATCH)
    # -----------------------------
    planner = db.relationship(
        "RelocationPlanner",
        back_populates="plans"
    )

    tasks = db.relationship(
        "Task",
        back_populates="plan",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    city = db.relationship(
        "City",
        back_populates="plans"
    )

    # -----------------------------
    # LOAD DEFAULT TASKS FROM TEMPLATE
    # -----------------------------
    def load_default_tasks(self):
        from core.domain.template_entity import TemplateTask
        from core.domain.task_entity import Task

        # prevent duplicate loading
        if self.tasks:
            return self.tasks

        templates = TemplateTask.query.filter_by(city_id=self.city_id).all()

        tasks = []

        for temp in templates:
            task = Task(
                plan_id=self.id,
                title=temp.title,
                category=temp.category,
                status="pending",
                priority="medium"
            )
            db.session.add(task)
            tasks.append(task)

        return tasks  # commit handled in logic layer

    # -----------------------------
    # UPDATE PLAN STATUS
    # -----------------------------
    def update_plan(self, new_status):
        if new_status:
            self.status = new_status

    # -----------------------------
    # PROGRESS CALCULATION
    # -----------------------------
    def get_progress(self):
        total = len(self.tasks)

        if total == 0:
            return 0

        completed = sum(1 for t in self.tasks if t.status == "completed")

        return int((completed / total) * 100)

    # -----------------------------
    # TASK FILTERING
    # -----------------------------
    def get_pending_tasks(self):
        return [task for task in self.tasks if task.status != "completed"]

    def get_completed_tasks(self):
        return [task for task in self.tasks if task.status == "completed"]

    # -----------------------------
    # ADD CUSTOM TASK
    # -----------------------------
    def add_custom_task(self, title, category):
        from core.domain.task_entity import Task

        if not title:
            return None

        task = Task(
            plan_id=self.id,
            title=title.strip(),
            category=category.strip() if category else "custom",
            status="pending",
            priority="medium"
        )

        db.session.add(task)
        return task  # commit handled in logic layer

    # -----------------------------
    # STRING REPRESENTATION
    # -----------------------------
    def __repr__(self):
        return f"<RelocationPlan id={self.id} city={self.city_id}>"