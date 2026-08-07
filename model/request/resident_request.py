from dataclasses import dataclass

@dataclass
class ResidentRequest:
    full_name: str
    cpf: str
    phone: int
    address_id: int
    association_id: int

    @staticmethod
    def from_dict(data: dict) -> 'ResidentRequest':
        return ResidentRequest(
            full_name=data['full_name'],
            cpf=data['cpf'],
            phone=data['phone'],
            address_id=data['address_id'],
            association_id=data.get('association_id')
        )

