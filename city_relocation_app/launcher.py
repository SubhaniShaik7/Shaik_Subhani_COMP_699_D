from core.app_factory import create_application


# -----------------------------
# CREATE APP INSTANCE
# -----------------------------
app = create_application()


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=app.config.get("DEBUG", True)
    )