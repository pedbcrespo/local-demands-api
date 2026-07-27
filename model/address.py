from config.db_config import db

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(255), nullable=False)
    district = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)

    def __init__(self, street: str, city: str, state: str):
        self.street = street
        self.city = city
        self.state = state