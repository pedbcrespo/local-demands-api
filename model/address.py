from config.db_config import db

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)

    def __init__(self, street: str, district:str, city: str, state: str):
        self.street = street
        self.district = district
        self.city = city
        self.state = state

    def to_dict(self):
        return {
            'id': self.id,
            'street': self.street,
            'district': self.district,
            'city': self.city,
            'state': self.state
        }