from model.request.resident_request import ResidentRequest
from repository.resident_repository import ResidentRepository
from repository.demand_repository import DemandRepository
from model.resident import Resident
from service.token_service import TokenService

class ResidentService:
    def __init__(self, resident_repository: ResidentRepository, demand_repository: DemandRepository) -> None:
        self.resident_repository = resident_repository
        self.demand_repository = demand_repository

    def get_by_cpf(self, cpf: str) -> dict | None:
        resident = self.resident_repository.get_by_cpf(cpf)
        return resident.to_dict() if resident else None

    def create(self, resident_data: ResidentRequest) -> dict:
        resident = Resident(
            full_name=resident_data.full_name,
            cpf=resident_data.cpf,
            phone=resident_data.phone,
            address_id=resident_data.address_id
        )
        existing_resident = self.__verify_existing_resident(resident)
        if existing_resident != None:
            resident = existing_resident
        else:
            resident = self.resident_repository.create(resident)
        return resident.to_dict()

    def update(self, resident_id: int, data: ResidentRequest) -> dict | None:
        resident = self.resident_repository.get(resident_id)
        if not resident:
            return None
        for key, value in vars(data).items():
            if key == 'id' or key == 'cpf':
                continue
            setattr(resident, key, value)
        updated_resident = self.resident_repository.update(resident_id, resident)
        return updated_resident.to_dict() if updated_resident else None

    def delete(self, resident_id: int) -> dict:
        if self.__is_used_resident(resident_id):
            return {'success': False, 'message': 'Resident is correlated with existing demands and cannot be deleted.'}
        is_deleted = self.resident_repository.delete(resident_id)
        if not is_deleted:
            return {'success': False, 'message': 'Could not delete the resident'}
        return {'success': True, 'message': 'Resident deleted successfully'}

    def __verify_existing_resident(self, resident: Resident) -> bool:
        existing_resident = self.resident_repository.get_by_cpf(resident.cpf)
        return existing_resident

    def __is_used_resident(self, resident_id: int) -> bool:
        demand_list = self.demand_repository.get_by_resident_id(resident_id)
        return len(demand_list) > 0