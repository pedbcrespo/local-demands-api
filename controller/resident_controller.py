from flask import Blueprint, request, jsonify
from model.request.resident_request import ResidentRequest
from config.db_config import db
from service.address_service import AddressService
from service.resident_service import ResidentService
from repository.resident_repository import ResidentRepository
from config.const_config import BASE_URL

resident_bp = Blueprint('residentservice = ResidentService(ResidentRepository())', __name__, url_prefix=f'/{BASE_URL}/residents')

service = ResidentService(ResidentRepository())

@resident_bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    resident_request = ResidentRequest.from_dict(data)
    registered_resident = service.create(resident_request)
    return jsonify(registered_resident), 200

