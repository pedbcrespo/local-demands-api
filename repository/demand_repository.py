from config.db_config import db
from model.demand import Demand
from model.address import Address
from model.enums.status import Status

class DemandRepository:
    def get_all(self) -> list[Demand]:
        return [d for d in Demand.query.all()]    

    def get_by_id(self, demand_id: int) -> Demand:
        return Demand.query.filter_by(id=demand_id).first()

    def get_by_resident_id(self, resident_id: int) -> list[Demand]:
        return [d for d in Demand.query.filter_by(resident_id=resident_id).all()]

    def get_by_address_id(self, address_id: int) -> list[Demand]:
        return [d for d in Demand.query.filter_by(address_id=address_id).all()]

    def create(self, demand: Demand) -> Demand:
        existing_demand = Demand.query.filter_by(
            resident_id=demand.resident_id,
            address_id=demand.address_id,
            description=demand.description
        ).first()
        if existing_demand:
            return existing_demand
        db.session.add(demand)
        db.session.commit()
        return demand

    def update(self, demand_id: int, data: Demand) -> Demand | None:
        demand = db.session.get(Demand, demand_id)
        if not demand:
            return None
        demand.resident_id = data.resident_id
        demand.address_id = data.address_id
        demand.description = data.description
        demand.status = data.status
        db.session.commit()
        return demand

    def finish(demand_id: int) -> bool:
        demand = db.session.get(Demand, demand_id)
        if not demand:
            return False
        demand.status = Status.FINISHED
        db.session.commit()
        return True

    def delete(self, demand_id: int) -> bool:
        demand = db.session.get(Demand, demand_id)
        if not demand:
            return False
        db.session.delete(demand)
        db.session.commit()
        return True