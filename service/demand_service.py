from repository.demand_repository import DemandRepository
from model.demand import Demand

class DemandService:
    def __init__(self, demand_repository: DemandRepository) -> None:
        self.demand_repository = demand_repository

    def get(self, demand_id: int) -> dict | None:
        return self.demand_repository.get(demand_id)

    def get_all(self) -> list[dict]:
        return self.demand_repository.get_all()

    def get_by_resident_id(self, resident_id: int) -> list[dict]:
        return self.demand_repository.get_by_resident_id(resident_id)   

    def get_by_address(self, address) -> list[dict]:
        return self.demand_repository.get_by_address(address)

    def create(self, demand_data: Demand) -> dict:
        return self.demand_repository.create(demand_data)

    def update(self, demand_id: int, updated_data: Demand) -> dict | None:
        return self.demand_repository.update(demand_id, updated_data)

    def delete(self, demand_id: int) -> bool:
        return self.demand_repository.delete(demand_id)