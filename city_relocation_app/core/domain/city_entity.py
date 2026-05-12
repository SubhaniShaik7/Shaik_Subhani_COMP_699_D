from core.db_extensions import db
from datetime import datetime


class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -----------------------------
    # RELATIONSHIPS (FIXED)
    # -----------------------------
    services = db.relationship(
        "CityService",
        backref="city",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    templates = db.relationship(
        "TemplateTask",
        backref="city",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # 🔥 THIS WAS MISSING (CRITICAL FIX)
    plans = db.relationship(
        "RelocationPlan",
        back_populates="city",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # -----------------------------
    # LOAD TASK TEMPLATES
    # -----------------------------
    def load_task_templates(self):
        return sorted(self.templates, key=lambda t: t.id)

    # -----------------------------
    # LOAD SERVICE LIST
    # -----------------------------
    def load_service_list(self):
        return sorted(self.services, key=lambda s: s.id)

    # -----------------------------
    # NORMALIZE DATA
    # -----------------------------
    def normalize(self):
        if self.name:
            self.name = self.name.strip()

        if self.state:
            self.state = self.state.strip()

        if self.country:
            self.country = self.country.strip()

    # -----------------------------
    # STRING REPRESENTATION
    # -----------------------------
    def __repr__(self):
        return f"<City id={self.id} name={self.name}>"