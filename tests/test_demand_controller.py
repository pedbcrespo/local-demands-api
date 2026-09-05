from config.db_config import db
from model import Address, Resident, Demand
from model.enums import State, DemandType
from model.enums.status import Status


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

def test_list_demands(client, app):
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
            cpf='12345678910',
            phone="22999999999",
            address_id=1
        )
        resident.id = 1
        db.session.add_all([resident])
        db.session.commit()

        demand = Demand(
            title="Test Demand",
            description="A description",
            address_id=1,
            resident_id=1,
            type=DemandType.STRUCTURAL.value
        )
        demand.id = 1
        db.session.add_all([demand])
        db.session.commit()

    response = client.get(f"{BASE_URL_DEMANDS}")
    assert response.status_code == 200
    assert len(response.json) > 0

def test_finish_demand(client, app):
    TEST_DEMAND_ID = 1
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
            cpf='12345678910',
            phone="22999999999",
            address_id=1
        )
        resident.id = 1
        db.session.add_all([resident])
        db.session.commit()

        demand = Demand(
            title="Test Demand",
            description="A description",
            address_id=1,
            resident_id=1,
            type=DemandType.STRUCTURAL.value
        )
        demand.id = TEST_DEMAND_ID
        db.session.add_all([demand])
        db.session.commit()

    response = client.put(f"{BASE_URL_DEMANDS}/{TEST_DEMAND_ID}/finish")
    assert response.status_code == 200
    assert response.json.get('status') == Status.FINISHED.value


def test_finish_demand_finished(client, app):
    TEST_DEMAND_ID = 1
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
            cpf='12345678910',
            phone="22999999999",
            address_id=1
        )
        resident.id = 1
        db.session.add_all([resident])
        db.session.commit()

        demand = Demand(
            title="Test Demand",
            description="A description",
            address_id=1,
            resident_id=1,
            type=DemandType.STRUCTURAL.value
        )
        demand.id = TEST_DEMAND_ID
        demand.status = Status.FINISHED
        db.session.add_all([demand])
        db.session.commit()

    response = client.put(f"{BASE_URL_DEMANDS}/{TEST_DEMAND_ID}/finish")
    assert response.status_code == 200
    assert response.json['id'] == None 

def test_delete_demand(client, app):
    TEST_DEMAND_ID = 1
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
            cpf='12345678910',
            phone="22999999999",
            address_id=1
        )
        resident.id = 1
        db.session.add_all([resident])
        db.session.commit()

        demand = Demand(
            title="Test Demand",
            description="A description",
            address_id=1,
            resident_id=1,
            type=DemandType.STRUCTURAL.value
        )
        demand.id = TEST_DEMAND_ID
        db.session.add_all([demand])
        db.session.commit()

    response = client.delete(f"{BASE_URL_DEMANDS}/{TEST_DEMAND_ID}/delete")
    assert response.status_code == 200
    assert response.json['success']

def test_delete_finished_demand(client, app):
    TEST_DEMAND_ID = 1
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
            cpf='12345678910',
            phone="22999999999",
            address_id=1
        )
        resident.id = 1
        db.session.add_all([resident])
        db.session.commit()

        demand = Demand(
            title="Test Demand",
            description="A description",
            address_id=1,
            resident_id=1,
            type=DemandType.STRUCTURAL.value
        )
        demand.id = TEST_DEMAND_ID
        demand.status = Status.FINISHED
        db.session.add_all([demand])
        db.session.commit()

    response = client.delete(f"{BASE_URL_DEMANDS}/{TEST_DEMAND_ID}/delete")
    print(response.json)
    assert response.status_code == 400
    assert not response.json['success']


