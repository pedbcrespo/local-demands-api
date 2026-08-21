from config.db_config import db

class Resident(db.Model):
    __tablename__ = 'resident'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)

    address = db.relationship('Address', lazy='joined')

    def __init__(self, full_name: str, cpf: str, phone: str, address_id: int):
        self.full_name = full_name
        self.cpf = cpf
        self.phone = phone
        self.address_id = address_id

    def to_dict(self):
        return {
            'cpf': self.cpf,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address.to_dict() if self.address else None,
        }