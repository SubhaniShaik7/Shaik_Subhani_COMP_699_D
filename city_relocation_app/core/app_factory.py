from flask import Flask
from core.settings import Config
from core.db_extensions import db, login_manager, bcrypt


# -----------------------------
# APPLICATION FACTORY
# -----------------------------
def create_application():
    app = Flask(__name__)
    app.config.from_object(Config)

    # fallback secret key (safety)
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "dev-secret-key"

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    configure_login(app)

    # register routes
    register_routes(app)

    # create database tables safely
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("Database initialization error:", str(e))

    # start scheduler (only if enabled)
    if app.config.get("ENABLE_SCHEDULER", True):
        start_background_jobs(app)

    return app


# -----------------------------
# LOGIN MANAGER SETUP
# -----------------------------
def configure_login(app):
    from core.domain.user_entity import User

    login_manager.login_view = "auth.home"
    login_manager.login_message = "Please login to continue"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception:
            return None


# -----------------------------
# REGISTER BLUEPRINTS
# -----------------------------
def register_routes(app):
    from core.endpoints.auth_endpoints import auth_bp
    from core.endpoints.planner_endpoints import planner_bp
    from core.endpoints.task_endpoints import task_bp
    from core.endpoints.dashboard_endpoints import dashboard_bp
    from core.endpoints.admin_endpoints import admin_bp
    from core.endpoints.misc_endpoints import misc_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(misc_bp)


# -----------------------------
# START BACKGROUND JOBS
# -----------------------------
def start_background_jobs(app):
    from core.helpers.scheduler_engine import start_scheduler

    try:
        start_scheduler(app)
    except Exception as e:
        print("Scheduler failed to start:", str(e))