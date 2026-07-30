from repository.demand_repository import DemandRepository
from repository.address_repository import AddressRepository
from model.demand import Demand
from model.address import Address
from model.resident import Resident

class DemandService:
    def __init__(self, demand_repository: DemandRepository, address_repository: AddressRepository) -> None:
        self.demand_repository = demand_repository
        self.address_repository = address_repository

    def get_all(self) -> list[dict]:
        demands = self.demand_repository.get_all()
        return [demand.to_dict() for demand in demands]

    def get_by_address(self, address_req: Address) -> list[dict]:
        address = self.address_repository.get(address_req.id)
        if not address:
            return []
        demands = self.demand_repository.get_by_address_id(address.id)
        return [demand.to_dict() for demand in demands]

    def get_by_resident(self, resident: Resident) -> list[dict]:
        demands = self.demand_repository.get_by_resident_id(resident.id)
        return [demand.to_dict() for demand in demands]