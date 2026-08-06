from model.request.address_request import AddressRequest
from model.request.demand_request import DemandRequest
from repository.demand_repository import DemandRepository
from repository.address_repository import AddressRepository
from repository.resident_repository import ResidentRepository
from model.demand import Demand
from model.enums import DemandType, Status
from service.token_service import TokenService

class DemandService:
    def __init__(self, demand_repository: DemandRepository, address_repository: AddressRepository, resident_repository: ResidentRepository) -> None:
        self.demand_repository = demand_repository
        self.address_repository = address_repository
        self.token_service = TokenService()

    def get_all(self) -> list[dict]:
        demands = self.demand_repository.get_all()
        return [demand.to_dict() for demand in demands]

    def create(self, token: str, demand_data: DemandRequest) -> dict | None:
        if not self.__validate_request(token):
            return None
        
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

    def finish(self, token: str, resident_id: int, demand_id: int) -> bool:
        manager = self.resident_repository.get(resident_id)
        if not manager or manager.type != 'manager':
            return False
        if not self.__validate_request(token):
            return False
        return self.demand_repository.finish(demand_id)

    def delete(self, token: str, demand_id: int) -> bool:
        if not self.__validate_request(token):
            return False

        demand = self.demand_repository.get_by_id(demand_id)
        if demand == None or demand.status == Status.FINISHED:
            return False
        self.demand_repository.delete(demand_id)
        return True

    def __verify_existing_resident_and_address(self, resident_id: int, address_id: int) -> bool:
        existing_resident = self.resident_repository.get(resident_id)
        existing_address = self.address_repository.get(address_id)
        if not existing_resident or not existing_address:
            return False
        return True

    def __validate_request(self, token: str) -> bool:
        payload = self.token_service.decode_token(token)
        return 'error' not in payload and payload['type'] == 'resident'