from config.db_config import db
from model import Address, Resident
from model.enums import State 

BASE_URL = "/local-demands/residents"

def test_create_resident(client, app):
    with app.app_context():
        add1 = Address(
            street="Av. Atlântica",
            district="Copacabana",
            city="Rio de Janeiro",
            state=State.RJ.code
        )
        add1.id = 1
        db.session.add_all([add1])
        db.session.commit()

    resident_request = {
            "full_name": "Fulano de Teste Testado",
            "cpf": "32112332112",
            "phone": "22998765432",
            "address_id": 1
        }
    
    response = client.post(f"{BASE_URL}/register", json=resident_request)
    assert response.status_code == 200
    assert response.json["cpf"] == "32112332112"

def test_login_success(client, app):
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

    response = client.post(f"{BASE_URL}/login", json={"cpf": TEST_CPF})
    assert response.status_code == 200
    assert response.json.get('id') is not None
    assert response.json.get('token') is not None


def test_update_resident(client, app):
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

    PHONE_TEST = "22997845162"

    response = client.post(f"{BASE_URL}/login", json={"cpf": TEST_CPF})
    login_resident = response.json
    login_resident['phone'] = PHONE_TEST
    login_resident['address_id'] = 1
    token = login_resident['token']
    response = client.put(f"{BASE_URL}/update/{login_resident['id']}", json=login_resident, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json.get('phone') is not None and response.json.get('phone') == PHONE_TEST
    
