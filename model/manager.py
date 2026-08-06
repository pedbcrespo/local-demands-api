from sqlalchemy import Date
from datetime import date
from model.resident import Resident
from config.db_config import db

class Manager(Resident):
    __tablename__ = 'manager'

    id = db.Column(db.Integer, db.ForeignKey('resident.id'), primary_key=True)
    start = db.Column(db.Date, nullable=False, default=date.today)
    finish = db.Column(db.Date, nullable=True)

    association = db.relationship('Association', back_populates='manager', lazy='joined', overlaps="residents")

    __mapper_args__ = {
        'polymorphic_identity': 'manager',
    }

    def __init__(self, full_name: str, cpf: str, phone: str, address_id: int, start: str = None, finish: str = None):
        super().__init__(full_name, cpf, phone, address_id)
        self.start = start if start else Date.today()
        self.finish = finish

    def to_dict(self):
        return {
            **super().to_dict(),
            'start': self.start,
            'finish': self.finish,
        }