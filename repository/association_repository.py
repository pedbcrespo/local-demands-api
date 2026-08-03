from config.db_config import db
from model.association import Association

class AssociationRepository:
    def create(self, resident_id: int, address_id: int, name: str) -> Association | None:
        existing_association = Association.query.filter_by(address_id=address_id, name=name).first()
        if existing_association:
            return existing_association
        association = Association(resident_id=resident_id, address_id=address_id, name=name)
        db.session.add(association)
        db.session.commit()
        return association