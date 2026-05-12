from core.db_extensions import db
from core.domain.city_entity import City
from core.domain.template_entity import TemplateTask
from core.domain.service_entity import CityService
from core.domain.planner_entity import RelocationPlanner
from core.domain.user_entity import User


# -----------------------------
# CREATE CITY
# -----------------------------
def create_city(name, state=None, country=None):
    try:
        if not name:
            return None

        name = name.strip()

        existing = City.query.filter_by(name=name).first()
        if existing:
            return existing  # avoid duplicates

        city = City(
            name=name,
            state=state.strip() if state else None,
            country=country.strip() if country else None
        )

        db.session.add(city)
        db.session.commit()

        return city

    except Exception:
        db.session.rollback()
        return None


# -----------------------------
# ADD TEMPLATE TASK
# -----------------------------
def add_template(city_id, category, title):
    try:
        if not city_id or not title:
            return None

        template = TemplateTask(
            city_id=city_id,
            category=category.strip() if category else "general",
            title=title.strip()
        )

        db.session.add(template)
        db.session.commit()

        return template

    except Exception:
        db.session.rollback()
        return None


# -----------------------------
# UPDATE TEMPLATE
# -----------------------------
def update_template(template_id, new_title=None, new_category=None):
    try:
        template = TemplateTask.query.get(template_id)
        if not template:
            return None

        template.update_template(
            new_title=new_title.strip() if new_title else None,
            new_category=new_category.strip() if new_category else None
        )

        db.session.commit()
        return template

    except Exception:
        db.session.rollback()
        return None


# -----------------------------
# LOAD HOUSING DATA
# -----------------------------
def load_housing_data(city_id, name, address):
    return _add_service(city_id, "housing", name, address)


# -----------------------------
# LOAD UTILITY DATA
# -----------------------------
def load_utility_data(city_id, name, address):
    return _add_service(city_id, "utility", name, address)


# -----------------------------
# LOAD DOCUMENT DATA
# -----------------------------
def load_document_data(city_id, name, address):
    return _add_service(city_id, "document", name, address)


# -----------------------------
# LOAD SERVICE LISTS
# -----------------------------
def load_service(city_id, name, address, service_type):
    return _add_service(city_id, service_type, name, address)


# -----------------------------
# INTERNAL SERVICE CREATOR
# -----------------------------
def _add_service(city_id, service_type, name, address):
    try:
        if not city_id or not name or not service_type:
            return None

        service = CityService(
            city_id=city_id,
            type=service_type.strip(),
            name=name.strip(),
            address=address.strip() if address else None
        )

        db.session.add(service)
        db.session.commit()

        return service

    except Exception:
        db.session.rollback()
        return None


# -----------------------------
# REFRESH DATASETS
# -----------------------------
def refresh_all_data():
    try:
        templates = TemplateTask.query.all()
        services = CityService.query.all()

        for t in templates:
            db.session.delete(t)

        for s in services:
            db.session.delete(s)

        db.session.commit()
        return True

    except Exception:
        db.session.rollback()
        return False


# =====================================================
# 🆕 PLANNER MANAGEMENT (ADMIN CONTROL - YOUR REQUIREMENT)
# =====================================================

# -----------------------------
# CREATE PLANNER FOR USER
# -----------------------------
def create_planner_for_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return None

        existing = RelocationPlanner.query.filter_by(user_id=user_id).first()
        if existing:
            return existing  # already exists

        planner = RelocationPlanner(user_id=user_id)

        db.session.add(planner)
        db.session.commit()

        return planner

    except Exception:
        db.session.rollback()
        return None


# -----------------------------
# GET ALL PLANNERS
# -----------------------------
def get_all_planners():
    try:
        return RelocationPlanner.query.all()
    except Exception:
        return []


# -----------------------------
# DELETE PLANNER
# -----------------------------
def delete_planner(user_id):
    try:
        planner = RelocationPlanner.query.filter_by(user_id=user_id).first()
        if not planner:
            return False

        db.session.delete(planner)
        db.session.commit()
        return True

    except Exception:
        db.session.rollback()
        return False


# -----------------------------
# ASSIGN PLANNER (SAFE LINK)
# -----------------------------
def assign_planner(user_id):
    """
    Ensures planner exists for user (safe operation)
    """
    try:
        planner = RelocationPlanner.query.filter_by(user_id=user_id).first()

        if not planner:
            planner = RelocationPlanner(user_id=user_id)
            db.session.add(planner)
            db.session.commit()

        return planner

    except Exception:
        db.session.rollback()
        return None