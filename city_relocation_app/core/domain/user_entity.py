from core.db_extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # -----------------------------
    # BASIC INFO
    # -----------------------------
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="user")  # user / admin

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # -----------------------------
    # RELATIONSHIP: PLANNER (ONE-TO-ONE)
    # -----------------------------
    planner = db.relationship(
        "RelocationPlanner",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined"
    )

    # -----------------------------
    # 🔥 ADMIN RELATIONSHIP (FIX)
    # -----------------------------
    admin = db.relationship(
        "SystemAdmin",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined"
    )

    # -----------------------------
    # PASSWORD METHODS
    # -----------------------------
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # -----------------------------
    # ROLE HELPERS
    # -----------------------------
    def is_admin(self):
        return self.role == "admin"

    # -----------------------------
    # PLANNER HELPER (IMPORTANT FIX)
    # -----------------------------
    def get_planner(self):
        """
        Always returns planner.
        If not exists, creates automatically.
        """
        from core.domain.planner_entity import RelocationPlanner

        if not self.planner:
            planner = RelocationPlanner(user_id=self.id)
            db.session.add(planner)
            db.session.commit()
            return planner

        return self.planner

    # -----------------------------
    # OPTIONAL: SAFE ADMIN CHECK
    # -----------------------------
    def get_admin(self):
        """
        Returns admin profile if exists
        """
        return self.admin

    # -----------------------------
    # STRING REPRESENTATION
    # -----------------------------
    def __repr__(self):
        return f"<User id={self.id}, email={self.email}, role={self.role}>"