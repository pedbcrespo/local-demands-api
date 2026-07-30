
from repository.address_repository import AddressRepository
from model.address import Address

class AddressService:
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository

    def get_cities_by_state(self, state: str) -> list[dict]:
        if not state:
            return []
        address = Address(state=state)
        return [add.to_dict() for add in self.address_repository.get_by_address(address)]

    def get_addresses_by_state_and_city(self, state: str, city: str) -> list[dict]:
        if not state or not city:
            return []
        address = Address(state=state, city=city)
        return [add.to_dict() for add in self.address_repository.get_by_address(address)]

    def create(self, address_data: Address) -> dict | None:
        saved_address = self.address_repository.create(address_data)
        return saved_address.to_dict() if saved_address else None

    def delete(self, address_id: int) -> bool:
        is_deleted = self.address_repository.delete(address_id)
        return is_deleted