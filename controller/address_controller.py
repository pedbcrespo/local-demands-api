from flask import Blueprint, request, jsonify
from model.request.address_request import AddressRequest
from service.address_service import AddressService
from repository.address_repository import AddressRepository
from config.const_config import BASE_URL

address_bp = Blueprint('address', __name__, url_prefix=f'/{BASE_URL}/address')

service = AddressService(AddressRepository())

@address_bp.route('/state', methods=['GET'])
def get_states():
    states = service.get_states()
    return jsonify(states), 200

@address_bp.route('/state/<state>', methods=['GET'])
def get_cities_by_state(state: str):
    states = service.get_cities_by_state(state)
    return jsonify(states), 200

@address_bp.route('/state/<state>/city/<city>', methods=['GET'])
def get_addresses_by_state_and_city(state: str, city: str):
    addresses = service.get_addresses_by_state_and_city(state, city)
    return jsonify(addresses), 200

@address_bp.route('/register', methods=['POST'])
def create():
    data = request.get_json(silent=True)
    address_request = AddressRequest.from_dict(data)
    if not address_request:
        return jsonify({'error': 'JSON inválido'}), 400
    address = service.create(address_request)
    return jsonify(address), 201

@address_bp.route('/delete/<int:address_id>', methods=['DELETE'])
def delete(address_id: int):
    is_deleted = service.delete(address_id)
    if is_deleted:
        return jsonify({'message': 'Endereço excluído com sucesso'}), 200
    else:
        return jsonify({'error': 'Endereço não encontrado'}), 404

