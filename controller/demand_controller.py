from flask import Blueprint, request, jsonify
from repository.demand_repository import DemandRepository
from repository.address_repository import AddressRepository
from repository.resident_repository import ResidentRepository
from service.demand_service import DemandService
from model.request.demand_request import DemandRequest
from config.const_config import BASE_URL

demand_bp = Blueprint('demand', __name__, url_prefix=f'/{BASE_URL}/demands')

service = DemandService(DemandRepository(), AddressRepository(), ResidentRepository())

@demand_bp.route('', methods=['GET'])
def list():
    demands = service.get_all()
    return jsonify(demands), 200

@demand_bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    token = get_token()
    demand_request = DemandRequest.from_dict(data)
    demand = service.create(token, demand_request)
    if not demand:
        return jsonify({'error': 'Failed to create demand'}), 400
    return jsonify(demand), 200

@demand_bp.route('/<int:demand_id>/finish', methods=['PUT'])
def finish(demand_id: int):
    data = request.get_json()
    token = get_token()
    resident_id = data.get('resident_id')
    success = service.finish(token, resident_id, demand_id)
    if not success:
        return jsonify({'error': 'Failed to finish demand'}), 400
    return jsonify({'message': 'Demand finished successfully'}), 200

@demand_bp.route('/<int:demand_id>/delete', methods=['DELETE'])
def delete(demand_id: int):
    token = get_token()
    success = service.delete(token, demand_id)
    if not success:
        return jsonify({'error': 'Failed to delete demand'}), 400
    return jsonify({'message': 'Demand deleted successfully'}), 200

def get_token():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    return token