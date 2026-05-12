from core.db_extensions import db
from core.domain.user_entity import User
from core.domain.planner_entity import RelocationPlanner
from core.domain.admin_entity import SystemAdmin
from flask_login import login_user, logout_user


# -----------------------------
# REGISTER USER
# -----------------------------
def register_user(username, email, password, role="user"):
    try:
        email = email.strip().lower()

        # check existing user
        existing = User.query.filter_by(email=email).first()
        if existing:
            return "exists"

        # create user
        user = User(
            username=username.strip(),
            email=email,
            role=role
        )

        # ✅ FIX: correct password method
        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        # ✅ FIX: ALWAYS create planner (IMPORTANT)
        planner = RelocationPlanner(user_id=user.id)
        db.session.add(planner)

        # optional admin entity
        if role == "admin":
            admin = SystemAdmin(user_id=user.id)
            db.session.add(admin)

        db.session.commit()

        return user

    except Exception as e:
        db.session.rollback()
        print("REGISTER ERROR:", str(e))
        return "error"


# -----------------------------
# LOGIN USER
# -----------------------------
def login_account(email, password):
    try:
        email = email.strip().lower()

        user = User.query.filter_by(email=email).first()

        if not user:
            print("LOGIN FAILED: user not found")
            return None

        # ✅ FIX: correct password check
        if not user.check_password(password):
            print("LOGIN FAILED: wrong password")
            return None

        login_user(user)
        return user

    except Exception as e:
        print("LOGIN ERROR:", str(e))
        return None


# -----------------------------
# LOGOUT USER
# -----------------------------
def logout_account():
    logout_user()


# -----------------------------
# UPDATE PROFILE
# -----------------------------
def update_profile(user_id, new_username):
    try:
        user = User.query.get(user_id)

        if not user or not new_username:
            return None

        user.username = new_username.strip()
        db.session.commit()

        return user

    except Exception as e:
        db.session.rollback()
        print("PROFILE UPDATE ERROR:", str(e))
        return None


# -----------------------------
# UPDATE ALERT PREFERENCE
# -----------------------------
def update_alert_settings(user_id, preference):
    try:
        if not preference:
            return None

        user = User.query.get(user_id)
        if not user:
            return None

        # ✅ FIX: use safe planner access
        planner = user.get_planner()
        planner.update_alert_preference(preference)

        db.session.commit()

        return planner

    except Exception as e:
        db.session.rollback()
        print("ALERT UPDATE ERROR:", str(e))
        return None


# -----------------------------
# PRIVACY ACCEPTANCE
# -----------------------------
def accept_privacy(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            return False

        # optional field check
        if hasattr(user, "privacy_accepted"):
            user.privacy_accepted = True

        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        print("PRIVACY ERROR:", str(e))
        return False