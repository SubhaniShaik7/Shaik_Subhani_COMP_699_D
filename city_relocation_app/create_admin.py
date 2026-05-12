from core.app_factory import create_application
from core.db_extensions import db
from core.domain.user_entity import User
from core.domain.admin_entity import SystemAdmin


def create_admin():
    app = create_application()

    with app.app_context():
        email = "admin@shaikcities.com"
        password = "Admin@123"

        existing = User.query.filter_by(email=email).first()

        if existing:
            print(" Admin already exists")
            return

        try:
            admin_user = User(
                username="ShaikCities Admin",   # FIXED
                email=email,
                role="admin"
            )

            admin_user.set_password(password)  # 

            db.session.add(admin_user)
            db.session.flush()

            admin = SystemAdmin(user_id=admin_user.id)
            db.session.add(admin)

            db.session.commit()

            print("===================================")
            print(" Admin created successfully")
            print("Email    : admin@shaikcities.com")
            print("Password : Admin@123")
            print("===================================")

        except Exception as e:
            db.session.rollback()
            print(" ERROR:", str(e))


if __name__ == "__main__":
    create_admin()