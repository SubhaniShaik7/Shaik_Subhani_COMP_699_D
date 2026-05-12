from core.db_extensions import db
from datetime import datetime


class TemplateTask(db.Model):
    __tablename__ = "template_tasks"

    id = db.Column(db.Integer, primary_key=True)

    city_id = db.Column(
        db.Integer,
        db.ForeignKey("cities.id"),
        nullable=False
    )

    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)

    default_priority = db.Column(db.String(20), default="medium")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -----------------------------
    # UPDATE TEMPLATE TASK
    # -----------------------------
    def update_template(self, new_title=None, new_category=None):
        if new_title:
            self.title = new_title.strip()

        if new_category:
            self.category = new_category.strip()

    # -----------------------------
    # STRING REPRESENTATION
    # -----------------------------
    def __repr__(self):
        return f"<TemplateTask id={self.id} title={self.title}>"