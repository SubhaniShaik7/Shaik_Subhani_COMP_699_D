from core.db_extensions import db
from core.domain.relocation_entity import RelocationPlan
from core.domain.city_entity import City
from core.domain.planner_entity import RelocationPlanner
from core.domain.template_entity import TemplateTask
from core.domain.task_entity import Task


# -----------------------------
# CREATE RELOCATION PLAN (FIXED)
# -----------------------------
def create_relocation_plan(planner_id, city_id):
    try:
        print("DEBUG: planner_id =", planner_id)
        print("DEBUG: city_id =", city_id)

        planner = RelocationPlanner.query.get(planner_id)
        city = City.query.get(city_id)

        if not planner:
            print("ERROR: Planner not found")
            return None

        if not city:
            print("ERROR: City not found")
            return None

        # ✅ CREATE PLAN
        plan = RelocationPlan(
            planner_id=planner_id,
            city_id=city_id
        )

        db.session.add(plan)
        db.session.flush()

        # ✅ LOAD TEMPLATE TASKS (SAFE)
        templates = TemplateTask.query.filter_by(city_id=city_id).all()

        print("DEBUG: templates found =", len(templates))

        for t in templates:
            task = Task(
                plan_id=plan.id,
                title=t.title,
                category=t.category,
                status="pending"
            )
            db.session.add(task)

        # ✅ EVEN IF NO TEMPLATES → PLAN STILL WORKS
        db.session.commit()

        print("SUCCESS: Plan created")
        return plan

    except Exception as e:
        db.session.rollback()
        print("CREATE PLAN ERROR:", str(e))
        return None


# -----------------------------
# SELECT CITY
# -----------------------------
def get_available_cities():
    try:
        return City.query.order_by(City.name).all()
    except Exception:
        return []


# -----------------------------
# VIEW TASKS BY CATEGORY
# -----------------------------
def get_tasks_by_category(plan_id, category):
    try:
        plan = RelocationPlan.query.get(plan_id)
        if not plan:
            return []

        return sorted(
            [task for task in plan.tasks if task.category == category],
            key=lambda t: t.id
        )

    except Exception:
        return []


# -----------------------------
# VIEW DASHBOARD
# -----------------------------
def get_dashboard_data(plan_id):
    try:
        plan = RelocationPlan.query.get(plan_id)
        if not plan:
            return None

        return {
            "progress": plan.get_progress(),
            "total_tasks": len(plan.tasks),
            "completed_tasks": len(plan.get_completed_tasks()),
            "pending_tasks": len(plan.get_pending_tasks())
        }

    except Exception:
        return None


# -----------------------------
# GET PENDING TASKS
# -----------------------------
def get_pending_tasks(plan_id):
    try:
        plan = RelocationPlan.query.get(plan_id)
        if not plan:
            return []

        return sorted(plan.get_pending_tasks(), key=lambda t: t.id)

    except Exception:
        return []


# -----------------------------
# GET COMPLETED TASKS
# -----------------------------
def get_completed_tasks(plan_id):
    try:
        plan = RelocationPlan.query.get(plan_id)
        if not plan:
            return []

        return sorted(plan.get_completed_tasks(), key=lambda t: t.id)

    except Exception:
        return []


# -----------------------------
# DOWNLOAD CHECKLIST
# -----------------------------
def generate_checklist(plan_id):
    try:
        plan = RelocationPlan.query.get(plan_id)
        if not plan:
            return []

        checklist = []

        for task in plan.tasks:
            checklist.append({
                "title": task.title,
                "status": task.status,
                "due_date": str(task.due_date) if task.due_date else None
            })

        return checklist

    except Exception:
        return []


# -----------------------------
# CLEAR COMPLETED TASKS
# -----------------------------
def clear_completed_tasks(plan_id):
    try:
        plan = RelocationPlan.query.get(plan_id)
        if not plan:
            return False

        completed_tasks = plan.get_completed_tasks()

        for task in completed_tasks:
            db.session.delete(task)

        db.session.commit()
        return True

    except Exception:
        db.session.rollback()
        return False