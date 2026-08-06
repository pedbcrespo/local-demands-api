
from model.request.address_request import AddressRequest
from repository.address_repository import AddressRepository
from model.address import Address
from model.enums import State

class AddressService:
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository

    def get_states(self):
        return State.get_state_codes()

    def get_cities_by_state(self, state: str) -> list[dict]:
        if not state:
            return []
    
        address_filter = Address(
            street=None,
            district=None,
            city=None,
            state=state
        )
        return [add.to_dict() for add in self.address_repository.get_by_address(address_filter)]

    def get_addresses_by_state_and_city(self, state: str, city: str) -> list[dict]:
        if not state or not city:
            return []
        address = Address(state=state, city=city)
        return [add.to_dict() for add in self.address_repository.get_by_address(address)]

    def create(self, address_data: AddressRequest) -> dict | None:
        address = Address(
            street=address_data.street,
            district=address_data.district,
            city=address_data.city,
            state=address_data.state
        )
        if self.__verify_existing_address(address):
            return None
        saved_address = self.address_repository.create(address)
        return saved_address.to_dict() if saved_address else None

    def delete(self, address_id: int) -> bool:
        is_deleted = self.address_repository.delete(address_id)
        return is_deleted

    def __verify_existing_address(self, address: Address) -> bool:
        existing_address = self.address_repository.get_by_address(address)
        return existing_address != None and len(existing_address) > 0
