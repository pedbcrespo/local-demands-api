
from repository.address_repository import AddressRepository
from model.address import Address

class AddressService:
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository

    def get_all(self) -> list[Address]:
        return self.address_repository.get_all()

    def get(self, address_id: int) -> Address | None:
        return self.address_repository.get(address_id)

    def get_addresses_by_state_and_city(self, state: str, city: str) -> list[Address]:
        if not state or not city:
            return []
        address = Address(state=state, city=city)
        return self.address_repository.get_by_address(address)

    def create(self, address_data: Address) -> Address | None:
        return self.address_repository.create(address_data)

    def update(self, address_id: int, address_data: Address) -> Address | None:
        return self.address_repository.update(address_id, address_data)

    def delete(self, address_id: int) -> bool:
        return self.address_repository.delete(address_id)