from core.db_extensions import db


class CityService(db.Model):
    __tablename__ = "city_services"

    id = db.Column(db.Integer, primary_key=True)

    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"), nullable=False)

    name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(50), nullable=False)  
    # examples: hospital, bank, store, utility, document, housing

    address = db.Column(db.String(250), nullable=True)

    contact_info = db.Column(db.String(150), nullable=True)

    # -----------------------------
    # CREATE SERVICE (Admin Feature)
    # -----------------------------
    def create_service(self):
        db.session.add(self)
        db.session.commit()

    # -----------------------------
    # UPDATE SERVICE
    # -----------------------------
    def update_service(self, name=None, service_type=None, address=None, contact_info=None):
        if name:
            self.name = name

        if service_type:
            self.type = service_type

        if address:
            self.address = address

        if contact_info:
            self.contact_info = contact_info

        db.session.commit()

    # -----------------------------
    # DELETE SERVICE
    # -----------------------------
    def delete_service(self):
        db.session.delete(self)
        db.session.commit()

    # -----------------------------
    # FILTER SERVICES BY TYPE
    # -----------------------------
    @staticmethod
    def get_services_by_type(city_id, service_type):
        return CityService.query.filter_by(city_id=city_id, type=service_type).all()

    # -----------------------------
    # GET ALL SERVICES FOR CITY
    # -----------------------------
    @staticmethod
    def get_all_services(city_id):
        return CityService.query.filter_by(city_id=city_id).all()

    def __repr__(self):
        return f"<Service {self.name} ({self.type})>"