from enum import Enum

class State(Enum):
    AC = ("AC", "Acre")
    AL = ("AL", "Alagoas")
    AP = ("AP", "Amapá")
    AM = ("AM", "Amazonas")
    BA = ("BA", "Bahia")
    CE = ("CE", "Ceará")
    DF = ("DF", "Distrito Federal")
    ES = ("ES", "Espírito Santo")
    GO = ("GO", "Goiás")
    MA = ("MA", "Maranhão")
    MT = ("MT", "Mato Grosso")
    MS = ("MS", "Mato Grosso do Sul")
    MG = ("MG", "Minas Gerais")
    PA = ("PA", "Pará")
    PB = ("PB", "Paraíba")
    PR = ("PR", "Paraná")
    PE = ("PE", "Pernambuco")
    PI = ("PI", "Piauí")
    RJ = ("RJ", "Rio de Janeiro")
    RN = ("RN", "Rio Grande do Norte")
    RS = ("RS", "Rio Grande do Sul")
    RO = ("RO", "Rondônia")
    RR = ("RR", "Roraima")
    SC = ("SC", "Santa Catarina")
    SP = ("SP", "São Paulo")
    SE = ("SE", "Sergipe")
    TO = ("TO", "Tocantins")

    def __init__(self, code: str, state_name: str):
        self.code = code
        self.state_name = state_name  # Alterado de self.name para self.state_name

    @classmethod
    def from_code(cls, code: str):
        code = code.upper().strip()
        for state in cls:
            if state.code == code:
                return state
        raise ValueError(f"'{code}' not found.")

    @classmethod
    def get_state_codes(cls) -> list[str]:
        return [state.code for state in cls]