import threading
import time
import logging
from core.logic.alert_logic import (
    process_reminders,
    generate_task_reminders,
    check_priority_alerts
)

# setup logger
logger = logging.getLogger("scheduler")
logger.setLevel(logging.INFO)


# -----------------------------
# SCHEDULER LOOP
# -----------------------------
def scheduler_loop(app, interval):
    logger.info("Scheduler started")

    while True:
        try:
            with app.app_context():
                generate_task_reminders()
                process_reminders()
                check_priority_alerts()

        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}")

        time.sleep(interval)


# -----------------------------
# START SCHEDULER
# -----------------------------
def start_scheduler(app):
    interval = app.config.get("REMINDER_INTERVAL", 60)

    # validate interval
    if not isinstance(interval, int) or interval <= 0:
        interval = 60

    # prevent multiple scheduler instances
    if getattr(app, "scheduler_started", False):
        logger.warning("Scheduler already running")
        return

    thread = threading.Thread(
        target=scheduler_loop,
        args=(app, interval),
        daemon=True,
        name="ReminderScheduler"
    )

    thread.start()

    # mark scheduler as started
    app.scheduler_started = True

    logger.info(f"Scheduler initialized with interval {interval} seconds")