from config.db_config import db
from model import Address
from model.enums import State 

BASE_URL = "/local-demands/address"

def test_create_address_success(client):
    payload = {
        "street": "Rua das Flores",
        "district": "Centro",
        "city": "Rio de Janeiro",
        "state": "RJ"
    }

    response = client.post(f"{BASE_URL}/register", json=payload)
    assert response.status_code == 200
    assert response.json["city"] == "Rio de Janeiro"

def test_get_states(client):
    response = client.get(f"{BASE_URL}/state")

    assert response.status_code == 200
    assert len(response.json) == 27
    assert "RJ" in response.json

def test_get_cities_by_state_success(client, app):
    response = client.get(f"{BASE_URL}/state/{State.RJ.code}")
    assert response.status_code == 200
    data = response.json
    
    assert len(data) == 92
    cities = [item["city_name"] for item in data]
    assert "Rio de Janeiro" in cities
    assert "Cabo Frio" in cities
    assert "São Paulo" not in cities

def test_delete_address(client, app):
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

    address_id = 1
    response = client.delete(f"{BASE_URL}/delete/{address_id}")

    assert response.status_code == 200
    assert response.json.get('error') is None