from repository.resident_repository import ResidentRepository
from model.resident import Resident


class ResidentService:
    def __init__(self, resident_repository: ResidentRepository) -> None:
        self.resident_repository = resident_repository

    def get(self, resident_id: int) -> dict | None:
        return self.resident_repository.get(resident_id)

    def get_by_name(self, name: str) -> list[dict]:
        return self.resident_repository.get_by_name(name)

    def create(self, resident_data: Resident) -> dict:
        return self.resident_repository.create(resident_data)

    def update(self, resident_id: int, resident_data: Resident) -> dict | None:
        return self.resident_repository.update(resident_id, resident_data)

    def delete(self, resident_id: int) -> bool:
        return self.resident_repository.delete(resident_id)