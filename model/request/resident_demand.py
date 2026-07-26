class ResidentDemand:
    def __init__(self, resident_id: int, demand_type: str, quantity: int):
        self.resident_id = resident_id
        self.demand_type = demand_type
        self.quantity = quantity

    def to_dict(self):
        return {
            "resident_id": self.resident_id,
            "demand_type": self.demand_type,
            "quantity": self.quantity
        }