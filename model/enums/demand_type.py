from enum import StrEnum

class DemandType(StrEnum):
    STRUCTURAL = 'STRUCTURAL'
    EMERGENCY = 'EMERGENCY'
    PERIODIC = 'PERIODIC'