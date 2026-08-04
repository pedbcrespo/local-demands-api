from dataclasses import dataclass

from model.request.demand_request import DemandRequest

@dataclass
class AddressRequest:
    street: str
    district: str
    city: str
    state: str

    @staticmethod
    def from_dict(data: dict) -> 'AddressRequest':
        return AddressRequest(
            street=data['street'],
            district=data['district'],
            city=data['city'],
            state=data['state']
        )

