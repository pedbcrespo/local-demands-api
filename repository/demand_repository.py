from config.db_config import db
from model.demand import Demand
from model.address import Address

class DemandRepository:
    def get_all(self) -> list[Demand]:
        return [d.to_dict() for d in Demand.query.all()]    

    def get_by_resident_id(self, resident_id: int) -> list[Demand]:
        return [d.to_dict() for d in Demand.query.filter_by(resident_id=resident_id).all()]

    def get_by_address(self, address: Address) -> list[Demand]:
        street = address.street
        city = address.city
        state = address.state
        return [d.to_dict() for d in Demand.query.join(Address).filter(
            Address.street == street,
            Address.city == city,
            Address.state == state
        ).all()]

    def get(self, demand_id: int) -> dict | None:
        demand = db.session.get(Demand, demand_id)
        return demand.to_dict() if demand else None

    def create(self, demand: Demand) -> dict:
        existing_demand = Demand.query.filter_by(
            resident_id=demand.resident_id,
            address_id=demand.address_id,
            description=demand.description
        ).first()
        if existing_demand:
            return existing_demand.to_dict()
        db.session.add(demand)
        db.session.commit()
        return demand.to_dict()

    def update(self, demand_id: int, data: Demand) -> dict | None:
        demand = db.session.get(Demand, demand_id)
        if not demand:
            return None
        demand.resident_id = data.resident_id
        demand.address_id = data.address_id
        demand.description = data.description
        demand.status = data.status
        db.session.commit()
        return demand.to_dict()

    def delete(self, demand_id: int) -> bool:
        demand = db.session.get(Demand, demand_id)
        if not demand:
            return False
        db.session.delete(demand)
        db.session.commit()
        return True