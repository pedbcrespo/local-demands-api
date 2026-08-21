from config.db_config import db
from model import Address, Resident
from model.enums import State, DemandType


BASE_URL = "/local-demands"
BASE_URL_DEMANDS = f"{BASE_URL}/demands"

def test_create_demand(client, app):
    TEST_CPF = "12345678910"
    TEST_RESIDENT_ID = 1
    with app.app_context():
        address = Address(
            street="Av. Atlântica",
            district="Copacabana",
            city="Rio de Janeiro",
            state=State.RJ.code
        )
        address.id = 1
        db.session.add_all([address])
        db.session.commit()

        resident = Resident(
            full_name="Fulano de Teste",
            cpf=TEST_CPF,
            phone="22999999999",
            address_id=1
        )
        resident.id = TEST_RESIDENT_ID
        db.session.add_all([resident])
        db.session.commit()

    demand_request = {
        "title": "Test Demand",
        "description": "A description to a test demand",
        "address_id": 1,
        "resident_id": TEST_RESIDENT_ID,
        "type": DemandType.STRUCTURAL.value
    }

    response = client.post(f"{BASE_URL_DEMANDS}", json=demand_request)
    assert response.status_code == 200  