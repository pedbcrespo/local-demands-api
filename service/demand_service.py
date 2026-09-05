from model.request.address_request import AddressRequest
from model.request.demand_request import DemandRequest
from repository.demand_repository import DemandRepository
from repository.address_repository import AddressRepository
from repository.resident_repository import ResidentRepository
from model.demand import Demand
from model.enums import DemandType, Status

class DemandService:
    def __init__(self, demand_repository: DemandRepository, address_repository: AddressRepository, resident_repository: ResidentRepository) -> None:
        self.demand_repository = demand_repository
        self.address_repository = address_repository
        self.resident_repository = resident_repository


    def get_all(self) -> list[dict]:
        demands = self.demand_repository.get_all()
        return [demand.to_dict() for demand in demands]

    def get_all_demand_types(self) -> list[str]:
        return [demant_type.value for demant_type in DemandType]

    def create(self, demand_data: DemandRequest) -> dict | None:
        if not self.__verify_existing_resident_and_address(demand_data.resident_id, demand_data.address_id):
            return None
        demand = Demand(
            title=demand_data.title,
            description=demand_data.description,
            address_id=demand_data.address_id,
            resident_id=demand_data.resident_id,
            type=DemandType(demand_data.type)
        )
        saved_demand = self.demand_repository.create(demand)
        return saved_demand.to_dict() if saved_demand else None

    def finish(self, demand_id: int) -> dict | None:
        demand = self.demand_repository.get(demand_id)
        if demand is None:
            return None
        if demand.status == Status.FINISHED:
            finished_response = Demand(None, None, None, None, None)
            finished_response.status = Status.FINISHED
            finished_response.created_at = None
            return finished_response
        isFinished = self.demand_repository.finish(demand_id)
        return demand.to_dict() if isFinished else None

    def delete(self, demand_id: int) -> dict | None:
        demand = self.demand_repository.get(demand_id)
        if demand == None or demand.status == Status.FINISHED:
            return {'success': False, 'message': 'Demand not found or already finished.'}
        self.demand_repository.delete(demand_id)
        return {'success': True, 'message': 'Demand deleted successfully.'}

    def __verify_existing_resident_and_address(self, resident_id: int, address_id: int) -> bool:
        existing_resident = self.resident_repository.get(resident_id)
        existing_address = self.address_repository.get(address_id)
        if not existing_resident or not existing_address:
            return False
        return True