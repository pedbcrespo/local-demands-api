
from repository.address_repository import AddressRepository
from model.address import Address

class AddressService:
    def __init__(self, address_repository: AddressRepository):
        self.address_repository = address_repository

    def get_all(self):
        return self.address_repository.get_all()

    def get(self, address_id: int):
        return self.address_repository.get(address_id)

    def create(self, address_data: Address):
        return self.address_repository.create(address_data)

    def update(self, address_id: int, address_data: Address):
        return self.address_repository.update(address_id, address_data)

    def delete(self, address_id: int):
        return self.address_repository.delete(address_id)