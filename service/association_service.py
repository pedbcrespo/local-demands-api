from repository.association_repository import AssociationRepository
from repository.resident_repository import ResidentRepository
from repository.address_repository import AddressRepository
from model.association import Association

class AssociationService:
    def __init__(self, association_repository):
        self.association_repository = association_repository

    def create(self, resident_id: int, address_id: int, name: str) -> dict | None:
        association = self.association_repository.create(resident_id, address_id, name)
        return association.to_dict() if association else None
    