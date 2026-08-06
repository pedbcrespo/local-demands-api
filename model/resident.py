from config.db_config import db

class Resident(db.Model):
    __tablename__ = 'resident'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    association_id = db.Column(db.Integer, db.ForeignKey('association.id'), nullable=True)
    type = db.Column(db.String(50))

    address = db.relationship('Address', lazy='joined')
    association = db.relationship('Association', back_populates='residents', lazy='joined')

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'resident',
    }

    def __init__(self, full_name: str, cpf: str, phone: str, address_id: int, association_id: int = None):
        self.full_name = full_name
        self.cpf = cpf
        self.phone = phone
        self.address_id = address_id
        self.association_id = association_id

    def to_dict(self):
        return {
            'cpf': self.cpf,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address.to_dict() if self.address else None,
            'association': self.association.name if self.association else None,
        }