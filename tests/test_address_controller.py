from config.db_config import db
from model.address import Address
from model.enums import State

def test_create_address_success(client):
    payload = {
        "street": "Rua das Flores",
        "district": "Centro",
        "city": "Rio de Janeiro",
        "state": "RJ"
    }

    response = client.post("/local-demands/address/register", json=payload)

    assert response.status_code == 201
    assert response.json["city"] == "Rio de Janeiro"

def test_get_states(client):
    response = client.get("/local-demands/address/state")

    assert response.status_code == 200
    assert len(response.json) == 27
    assert "RJ" in response.json

def test_get_cities_by_state_success(client, app):
    with app.app_context():
        add1 = Address(
            street="Av. Atlântica",
            district="Copacabana",
            city="Rio de Janeiro",
            state=State.RJ.code
        )
        add2 = Address(
            street="Rua das Conchas",
            district="Peró",
            city="Cabo Frio",
            state=State.RJ.code
        )
        add3 = Address(
            street="Av. Paulista",
            district="Bela Vista",
            city="São Paulo",
            state=State.SP.code
        )
        
        db.session.add_all([add1, add2, add3])
        db.session.commit()

    response = client.get(f"/local-demands/address/state/{State.RJ.code}")
    assert response.status_code == 200
    data = response.json
    
    assert len(data) == 2
    cities = [item["city"] for item in data]
    assert "Rio de Janeiro" in cities
    assert "Cabo Frio" in cities
    assert "São Paulo" not in cities
