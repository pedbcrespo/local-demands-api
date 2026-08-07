from config.db_config import db
from model.resident import Resident
from model.request import ResidentRequest


class ResidentRepository:
    def get_by_cpf(self, cpf: str) -> Resident | None:
        resident = Resident.query.filter_by(cpf=cpf).first()
        return resident

    def create(self, resident: Resident) -> Resident | None:
        db.session.add(resident)
        db.session.commit()
        return resident

    def update(self, resident_id: int, data: ResidentRequest) -> Resident | None:
        resident = db.session.get(Resident, resident_id)
        if not resident:
            return None
        resident.full_name = data.full_name
        resident.phone = data.phone
        resident.address_id = data.address_id
        if data.association_id is not None:
            resident.association_id = data.association_id
        db.session.commit()
        return resident

    def delete(self, resident_id: int) -> bool:
        resident = db.session.get(Resident, resident_id)
        if not resident:
            return False
        db.session.delete(resident)
        db.session.commit()
        return True

