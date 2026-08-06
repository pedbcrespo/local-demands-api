from flask import Blueprint, request, jsonify
from model.request import AddressRequest
from service import AddressService
from repository import AddressRepository, DemandRepository
from config.const_config import BASE_URL

address_bp = Blueprint('address', __name__, url_prefix=f'/{BASE_URL}/address')

service = AddressService(AddressRepository(), DemandRepository())

@address_bp.route('/state', methods=['GET'])
def get_states():
    states = service.get_states()
    if states == None:
        return jsonify({'error': 'Could not get the states'}), 400
    return jsonify(states), 200

@address_bp.route('/state/<state>', methods=['GET'])
def get_cities_by_state(state: str):
    cities = service.get_cities_by_state(state)
    if cities == None:
            return jsonify({'error': 'Could not get the cities'}), 400
    return jsonify(cities), 200

@address_bp.route('/register', methods=['POST'])
def create():
    data = request.get_json(silent=True)
    address_request = AddressRequest.from_dict(data)
    if not address_request:
        return jsonify({'error': 'JSON inválido'}), 400
    address = service.create(address_request)
    if address != None:
        jsonify(address), 200 
    return jsonify({'error': 'Could not register address'}), 400

@address_bp.route('/delete/<int:address_id>', methods=['DELETE'])
def delete(address_id: int):
    is_deleted = service.delete(address_id)
    if is_deleted:
        return jsonify({'message': 'Address deleted!'}), 200
    else:
        return jsonify({'error': 'Address could not be deleted, it is likely still in use.'}), 400

