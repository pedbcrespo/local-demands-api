from model.request.resident_request import ResidentRequest
from repository.resident_repository import ResidentRepository
from model.resident import Resident


class ResidentService:
    def __init__(self, resident_repository: ResidentRepository) -> None:
        self.resident_repository = resident_repository

    def get_all(self) -> list[dict]:
        residents = Resident.query.all()
        return [resident.to_dict() for resident in residents]

    def get_by_cpf(self, cpf: str) -> Resident | None:
        resident = self.resident_repository.get_by_cpf(cpf)
        return resident.to_dict() if resident else None

    def create(self, resident_data: ResidentRequest) -> dict:
        resident = Resident(
            full_name=resident_data.full_name,
            cpf=resident_data.cpf,
            phone=resident_data.phone,
            address_id=resident_data.address_id
        )
        if self.__verify_existing_resident(resident):
            return None
        registered_resident = self.resident_repository.create(resident)
        return registered_resident.to_dict() if registered_resident else None

    def update(self, resident_id: int, resident_data: ResidentRequest) -> dict | None:
        resident = Resident(
            full_name=resident_data.full_name,
            cpf=resident_data.cpf,
            phone=resident_data.phone,
            address_id=resident_data.address_id
        )
        updated_resident = self.resident_repository.update(resident_id, resident)
        return updated_resident.to_dict() if updated_resident else None

    def delete(self, resident_id: int) -> bool:
        is_deleted = self.resident_repository.delete(resident_id)
        return is_deleted

    def __verify_existing_resident(self, resident: Resident) -> bool:
        existing_resident = self.resident_repository.get_by_cpf(resident.cpf)
        return existing_resident != None