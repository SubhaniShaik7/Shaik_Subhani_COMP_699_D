from core.db_extensions import db
from datetime import datetime


class SystemAdmin(db.Model):
    __tablename__ = "system_admins"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True  # one user = one admin
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # -----------------------------
    # RELATIONSHIP (FIXED & MATCHED)
    # -----------------------------
    user = db.relationship(
        "User",
        back_populates="admin",
        lazy="joined"
    )

    # -----------------------------
    # ROLE CHECK
    # -----------------------------
    def is_admin(self):
        return True

    # -----------------------------
    # OPTIONAL HELPER
    # -----------------------------
    def get_user_email(self):
        return self.user.email if self.user else None

    # -----------------------------
    # STRING REPRESENTATION
    # -----------------------------
    def __repr__(self):
        return f"<SystemAdmin id={self.id}, user_id={self.user_id}>"