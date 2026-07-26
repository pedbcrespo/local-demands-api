from config.db_config import db
from model.resident import Resident


class ResidentRepository:
    def get_all(self) -> list[Resident]:
        return [r.to_dict() for r in Resident.query.all()]

    def get(self, resident_id: int) -> dict | None:
        resident = db.session.get(Resident, resident_id)
        return resident.to_dict() if resident else None

    def get_by_name(self, full_name: str) -> list[Resident]:
        return [r.to_dict() for r in Resident.query.filter_by(full_name=full_name).all()]

    def create(self, resident: Resident) -> dict:
        existing_resident = Resident.query.filter_by(full_name=resident.full_name, phone=resident.phone, address_id=resident.address_id).first()
        if existing_resident:
            return existing_resident.to_dict()
        db.session.add(resident)
        db.session.commit()
        return resident.to_dict()

    def update(self, resident_id: int, data: Resident) -> dict | None:
        resident = db.session.get(Resident, resident_id)
        if not resident:
            return None
        resident.full_name = data.get('full_name', resident.full_name)
        resident.phone = data.get('phone', resident.phone)
        db.session.commit()
        return resident.to_dict()

    def delete(self, resident_id: int) -> bool:
        resident = db.session.get(Resident, resident_id)
        if not resident:
            return False
        db.session.delete(resident)
        db.session.commit()
        return True

