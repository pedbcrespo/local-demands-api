from flask import Blueprint, request, jsonify
from model.request.resident_request import ResidentRequest
from config.db_config import db
from service.address_service import AddressService
from service.resident_service import ResidentService
from repository.resident_repository import ResidentRepository
from repository.association_repository import AssociationRepository
from config.const_config import BASE_URL

resident_bp = Blueprint('residentservice = ResidentService(ResidentRepository())', __name__, url_prefix=f'/{BASE_URL}/residents')

service = ResidentService(ResidentRepository(), AssociationRepository())

@resident_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cpf = data.get('cpf')
    resident = service.login(cpf)
    if not resident:
        return jsonify({'error': 'Resident not found'}), 404
    return jsonify(resident), 200

@resident_bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    resident_request = ResidentRequest.from_dict(data)
    registered_resident = service.create(resident_request)
    return jsonify(registered_resident), 200

@resident_bp.route('/<int:resident_id>', methods=['PUT'])
def update(resident_id: int):
    data = request.get_json()
    resident_request = ResidentRequest.from_dict(data)
    updated_resident = service.update(resident_id, resident_request)
    if not updated_resident:
        return jsonify({'error': 'Resident not found'}), 404
    return jsonify(updated_resident), 200

@resident_bp.route('/<resident_id>', methods=['DELETE'])
def delete(resident_id: int):
    is_deleted = service.delete(resident_id)
    if is_deleted:
        return jsonify({'message': 'Resident deleted successfully'}), 200
    else:
        return jsonify({'error': 'Resident not found'}), 404