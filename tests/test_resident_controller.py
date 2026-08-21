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

def test_get_resident(client, app):
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

        response = client.get(f"{BASE_URL}/{TEST_CPF}")
        assert response.status_code == 200
        assert 'id' in response.json

def test_update_resident(client, app):
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

    PHONE_TEST = "22997845162"

    request = {
        'full_name':"Fulano de Teste",
        'cpf':TEST_CPF,
        'phone':PHONE_TEST,
        'address_id':1
    }

    response = client.put(f"{BASE_URL}/update/{TEST_RESIDENT_ID}", json=request)

    assert response.status_code == 200
    assert response.json.get('phone') is not None and response.json.get('phone') == PHONE_TEST

def test_delete_resident(client, app):
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

    response = client.delete(f"{BASE_URL}/delete/{TEST_RESIDENT_ID}")

    assert response.status_code == 200
    assert response.json.get('error') is None
        
