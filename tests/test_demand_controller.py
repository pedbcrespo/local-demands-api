from config.db_config import db
from model import Address, Resident
from model.enums import State, DemandType


BASE_URL = "/local-demands"
BASE_URL_DEMANDS = f"{BASE_URL}/demands"
BASE_URL_LOGIN = f"{BASE_URL}/residents"

def test_create_demand(client, app):
    TEST_CPF = "12345678910"
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
        db.session.add_all([resident])
        db.session.commit()

    login_response = client.post(f"{BASE_URL_LOGIN}/login", json={"cpf": TEST_CPF})
    token = login_response.json.get('token')

    demand_request = {
        "title": "Test Demand",
        "description": "A description to a test demand",
        "address_id": 1,
        "resident_id": resident.id,
        "type": DemandType.STRUCTURAL.value
    }

    response = client.post(f"{BASE_URL_DEMANDS}", json=demand_request, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200  