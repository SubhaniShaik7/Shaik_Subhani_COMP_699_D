from core.domain.city_entity import City
from core.domain.service_entity import CityService


# -----------------------------
# GET ALL CITIES (Requirement 4)
# -----------------------------
def fetch_all_cities():
    try:
        return City.query.order_by(City.name).all()
    except Exception:
        return []


# -----------------------------
# GET CITY BY ID
# -----------------------------
def get_city_by_id(city_id):
    try:
        if not city_id:
            return None

        return City.query.get(city_id)

    except Exception:
        return None


# -----------------------------
# LOAD SERVICE LIST (17,18)
# -----------------------------
def get_city_services(city_id):
    try:
        if not city_id:
            return []

        services = CityService.get_all_services(city_id)

        return services if services else []

    except Exception:
        return []


# -----------------------------
# FILTER SERVICES BY TYPE
# -----------------------------
def get_services_by_type(city_id, service_type):
    try:
        if not city_id or not service_type:
            return []

        services = CityService.get_services_by_type(city_id, service_type)

        return services if services else []

    except Exception:
        return []


# -----------------------------
# GET CITY TEMPLATES
# -----------------------------
def get_city_templates(city_id):
    try:
        if not city_id:
            return []

        city = City.query.get(city_id)
        if not city:
            return []

        templates = city.load_task_templates()

        return templates if templates else []

    except Exception:
        return []