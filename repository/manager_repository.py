from config.db_config import db
from model.manager import Manager
from model.resident import Resident

class ManagerRepository:
    def create(self, resident: Resident) -> Manager | None:
        existing_manager = Manager.query.filter_by(id=resident.id).first()
        if existing_manager:
            return None
        manager = resident.to_manager()
        db.session.add(manager)
        db.session.commit()
        return manager

    def get_by_email(self, email: str) -> Manager | None:
        return Manager.query.filter_by(email=email).first()