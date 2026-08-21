from config.db_config import db 
from model.enums import Status, DemandType
import datetime

class Demand(db.Model):
    __tablename__ = 'demand'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    status = db.Column(db.Enum(Status), default=Status.PENDING, nullable=False)
    type = db.Column(db.Enum(DemandType), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    address = db.relationship('Address', lazy='joined')
    resident = db.relationship('Resident', lazy='joined')

    def __init__(self, title: str, description: str, address_id: int, resident_id: int, type: DemandType) -> None:
        self.title = title
        self.description = description
        self.address_id = address_id
        self.resident_id = resident_id
        self.type = type
        self.status = Status('PENDING')
        self.created_at = datetime.datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'address': self.address.to_dict() if self.address else None,
            'resident': self.resident.full_name if self.resident else None,
            'status': self.status.value,
            'type': self.type.value,
            'created_at': self.created_at.isoformat()
        }