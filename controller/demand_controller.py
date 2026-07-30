from flask import Blueprint, request, jsonify
from repository.demand_repository import DemandRepository
from repository.address_repository import AddressRepository
from service.demand_service import DemandService
from config.const_config import BASE_URL

demand_bp = Blueprint('demand', __name__, url_prefix=f'/{BASE_URL}/demand')

service = DemandService(DemandRepository(), AddressRepository())

@demand_bp.route('', methods=['GET'])
def list():
    demands = service.get_all()
    return jsonify(demands), 200