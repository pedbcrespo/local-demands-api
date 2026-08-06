from config.db_config import db
from model import Address
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