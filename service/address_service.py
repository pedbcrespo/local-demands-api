
from model.request import AddressRequest
from repository import AddressRepository, DemandRepository
from model import Address
from model.enums import State
from pathlib import Path
import json

class AddressService:
    def __init__(self, address_repository: AddressRepository, demand_repository: DemandRepository):
        self.address_repository = address_repository
        self.demand_repository = demand_repository

    def get_states(self):
        return State.get_state_codes()

    def get_cities_by_state(self, state: str) -> list[dict]:
        if not state:
            return []
        cities = self.__read_brazil_cities_json()
        filtered_cities = list(filter(lambda city: city['state_code'] == state, cities))
        return filtered_cities


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
            return address.to_dict()
        saved_address = self.address_repository.create(address)
        print(saved_address)
        return saved_address.to_dict() if saved_address != None else None

    def delete(self, address_id: int) -> bool:
        if self.__is_used_address(address_id):
            return False
        is_deleted = self.address_repository.delete(address_id)
        return is_deleted

    def __verify_existing_address(self, address: Address) -> bool:
        existing_address = self.address_repository.get_by_address(address)
        return existing_address != None and len(existing_address) > 0

    def __is_used_address(self, address_id: int) -> bool:
        address_list = self.demand_repository.get_by_address_id(address_id)
        return len(address_list) > 0

    def __read_brazil_cities_json(self):
        FILE_NAME = "brazil_cities.json"
        full_file_path = Path(__file__).resolve().parent.parent / FILE_NAME
        with open(full_file_path, mode='r', encoding='utf-8') as file:
            return json.load(file)


