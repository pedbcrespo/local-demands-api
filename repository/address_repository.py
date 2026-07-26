from config.db_config import db
from model.address import Address


class AddressRepository:
    def get_all(self) -> list[Address]:
        return [a.to_dict() for a in Address.query.all()]

    def get(self, address_id: int) -> dict | None:
        address = db.session.get(Address, address_id)
        return address.to_dict() if address else None

    def create(self, address: Address) -> dict:
        existing_address = Address.query.filter_by(street=address.street, city=address.city, state=address.state).first()
        if existing_address:
            return existing_address.to_dict()
        db.session.add(address)
        db.session.commit()
        return address.to_dict()

    def update(self, address_id: int, data: Address) -> dict | None:
        address = db.session.get(Address, address_id)
        if not address:
            return None
        address.street = data.get('street', address.street)
        address.city   = data.get('city', address.city)
        address.state  = data.get('state', address.state)
        db.session.commit()
        return address.to_dict()

    def delete(self, address_id: int) -> bool:
        address = db.session.get(Address, address_id)
        if not address:
            return False
        db.session.delete(address)
        db.session.commit()
        return True