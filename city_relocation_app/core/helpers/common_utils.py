from datetime import datetime


# -----------------------------
# FORMAT DATETIME
# -----------------------------
def format_datetime(value):
    if not value or not isinstance(value, datetime):
        return ""

    return value.strftime("%Y-%m-%d %H:%M")


# -----------------------------
# SAFE INTEGER CONVERSION
# -----------------------------
def to_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# -----------------------------
# EMPTY CHECK
# -----------------------------
def is_empty(value):
    if value is None:
        return True

    if isinstance(value, str):
        return value.strip() == ""

    return False


# -----------------------------
# STANDARD RESPONSE BUILDER
# -----------------------------
def build_response(success=True, message="", data=None):
    return {
        "success": bool(success),
        "message": message or "",
        "data": data
    }


# -----------------------------
# FLEXIBLE DATETIME PARSER
# -----------------------------
def parse_datetime(date_str):
    if not date_str:
        return None

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue

    return None