from flask import Blueprint, request, jsonify
from repository.demand_repository import DemandRepository
from repository.address_repository import AddressRepository
from repository.resident_repository import ResidentRepository
from service.demand_service import DemandService
from model.request.demand_request import DemandRequest
from config.const_config import BASE_URL

demand_bp = Blueprint('demand', __name__, url_prefix=f'/{BASE_URL}/demand')

service = DemandService(DemandRepository(), AddressRepository(), ResidentRepository())

@demand_bp.route('', methods=['GET'])
def list():
    demands = service.get_all()
    return jsonify(demands), 200


@demand_bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    demand_request = DemandRequest.from_dict(data)
    demand = service.create(demand_request)
    if not demand:
        return jsonify({'error': 'Failed to create demand'}), 400
    return jsonify(demand), 201