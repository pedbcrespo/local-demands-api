from config.db_config import db
from model.resident import Resident


class ResidentRepository:
    def get_by_cpf(self, cpf: str) -> Resident | None:
        resident = Resident.query.filter_by(cpf=cpf).first()
        return resident

    def create(self, resident: Resident) -> Resident | None:
        db.session.add(resident)
        db.session.commit()
        return resident

    def update(self, resident_id: int, data: Resident) -> Resident | None:
        resident = db.session.get(Resident, resident_id)
        if not resident:
            return None
        resident.full_name = data.get('full_name', resident.full_name)
        resident.phone = data.get('phone', resident.phone)
        db.session.commit()
        return resident

    def delete(self, resident_id: int) -> bool:
        resident = db.session.get(Resident, resident_id)
        if not resident:
            return False
        db.session.delete(resident)
        db.session.commit()
        return True

