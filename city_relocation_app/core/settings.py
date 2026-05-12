import os


# -----------------------------
# BASE DIRECTORY
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Config:
    # -----------------------------
    # SECURITY
    # -----------------------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # -----------------------------
    # DATABASE CONFIG
    # -----------------------------
    DB_PATH = os.path.join(BASE_DIR, "storage", "app_data.db")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{DB_PATH}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------------
    # SESSION CONFIG
    # -----------------------------
    SESSION_PERMANENT = False

    # -----------------------------
    # FILE STORAGE
    # -----------------------------
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "storage", "uploads")

    # -----------------------------
    # SCHEDULER CONFIG
    # -----------------------------
    REMINDER_INTERVAL = int(os.environ.get("REMINDER_INTERVAL", 60))

    ENABLE_SCHEDULER = os.environ.get("ENABLE_SCHEDULER", "true").lower() == "true"

    # -----------------------------
    # DEBUG MODE
    # -----------------------------
    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"