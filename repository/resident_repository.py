from config.db_config import db
from model.resident import Resident
from model.request import ResidentRequest


class ResidentRepository:
    def get(self, resident_id: int) -> Resident | None:
        resident = db.session.get(Resident, resident_id)
        return resident

    def get_by_cpf(self, cpf: str) -> Resident | None:
        resident = Resident.query.filter_by(cpf=cpf).first()
        return resident

    def create(self, resident: Resident) -> Resident | None:
        db.session.add(resident)
        db.session.commit()
        return resident

    def update(self, resident_id: int, data: Resident) -> Resident | None:
        resident = db.session.get(Resident, resident_id)
        data.id = resident_id
        resident = data
        db.session.commit()
        return resident

    def delete(self, resident_id: int) -> bool:
        resident = db.session.get(Resident, resident_id)
        if not resident:
            return False
        db.session.delete(resident)
        db.session.commit()
        return True

