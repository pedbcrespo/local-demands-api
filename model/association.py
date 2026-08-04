from config.db_config import db

class Association(db.Model):
    __tablename__ = 'association'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)

    address = db.relationship('Address', lazy='joined')
    residents = db.relationship('Resident', back_populates='association', lazy='select')
    manager = db.relationship('Manager', back_populates='association', uselist=False, lazy='joined')

    def __init__(self, name: str, address_id: int):
        self.name       = name
        self.address_id = address_id

    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address.to_dict() if self.address else None,
            'manager': self.manager.full_name if self.manager else None,
            'residents': self.__get_residents()
        }


    def __get_residents(self):
        filtered_residents = [resident for resident in self.residents if resident.id != self.manager.id]
        return filtered_residents