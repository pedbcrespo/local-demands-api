from dataclasses import dataclass

@dataclass
class DemandRequest:
    title: str
    description: str
    resident_id: int
    address_id: int
    type: str

    @staticmethod
    def from_dict(data: dict) -> 'DemandRequest':
        return DemandRequest(
            title=data['title'],
            description=data['description'],
            address_id=data['address_id'],
            type=data['type'],
            resident_id=data['resident_id'],
        )

