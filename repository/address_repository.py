from config.db_config import db
from model.address import Address

class AddressRepository:
    def get_by_address(self, address: Address) -> list:
        if not address:
            return []
        filters = []
        filter_cases = [
            {'case': lambda add: add.id, 'filter': lambda add: Address.id == add.id},
            {'case': lambda add: add.street, 'filter': lambda add: Address.street.ilike(f'%{add.street}%')},
            {'case': lambda add: add.district, 'filter': lambda add: Address.district.ilike(f'%{add.district}%')},
            {'case': lambda add: add.city, 'filter': lambda add: Address.city.ilike(f'%{add.city}%')},
            {'case': lambda add: add.state, 'filter': lambda add: Address.state.ilike(f'%{add.state}%')},
        ]

        for case in filter_cases:
            if case['case'](address):
                filters.append(case['filter'](address))
    
        if not filters:
            return []
        
        return [a.to_dict() for a in Address.query.filter(db.or_(*filters)).distinct().all()]

    def create(self, address: Address) -> dict | None:
        if not address:
            return None
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