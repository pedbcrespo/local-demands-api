from model.request.resident_request import ResidentRequest
from repository.resident_repository import ResidentRepository
from repository.association_repository import AssociationRepository
from model.resident import Resident
import jwt
from datetime import datetime, timedelta

class ResidentService:
    def __init__(self, resident_repository: ResidentRepository, association_repository: AssociationRepository) -> None:
        self.resident_repository = resident_repository
        self.association_repository = association_repository

    def get_by_association(self, association_id: int) -> list[dict]:
        association = self.association_repository.get_by_id(association_id)
        if not association:
            return []
        residents = Resident.query.filter(Resident.association_id == association_id).all()
        return [resident.to_dict() for resident in residents]

    def login(self, cpf: str) -> dict | None:
        resident = self.resident_repository.get_by_cpf(cpf)
        resident_dict = resident.to_dict() if resident else None
        if resident_dict:
            resident_dict.pop('token', self.__get_token(resident))
        return resident_dict

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

    def __get_token(self, resident: Resident) -> str:
        SECRET_KEY = 'chavesecreta1234567890'
        return jwt.encode(
        {
            'id': resident.id,
            'type': resident.type,
            'exp': timedelta(hours=8)
        },
        SECRET_KEY,
        algorithm='HS256'
    )
    