from flask import Blueprint, request, jsonify
from service.address_service import AddressService
from repository.address_repository import AddressRepository
from config.const_config import BASE_URL

address_bp = Blueprint('address', __name__, url_prefix=f'/{BASE_URL}/address')

service = AddressService(AddressRepository())


@address_bp.route('', methods=['GET'])
def list_addresses():
    addresses = service.get_all()
    return jsonify(addresses), 200


@address_bp.route('/state/<state>/city/<city>', methods=['GET'])
def get_addresses_by_state_and_city(state, city):
    addresses = service.get_addresses_by_state_and_city(state, city)
    return jsonify(addresses), 200



@address_bp.route('', methods=['POST'])
def create_address():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'JSON inválido'}), 400
    address = service.create_address(data)
    return jsonify(address), 201


@address_bp.route('/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'JSON inválido'}), 400
    address = service.update_address(address_id, data)
    if not address:
        return jsonify({'error': 'endereço não encontrado'}), 404
    return jsonify(address), 200


@address_bp.route('/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    success = service.delete_address(address_id)
    if not success:
        return jsonify({'error': 'endereço não encontrado'}), 404
    return jsonify({'message': 'endereço deletado com sucesso'}), 200