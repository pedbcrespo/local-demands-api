from flask import Blueprint, request, jsonify
from model.request.resident_request import ResidentRequest
from config.db_config import db
from service.resident_service import ResidentService
from repository.resident_repository import ResidentRepository
from config.const_config import BASE_URL

resident_bp = Blueprint('residentservice = ResidentService(ResidentRepository())', __name__, url_prefix=f'/{BASE_URL}/residents')

service = ResidentService(ResidentRepository())

@resident_bp.route('/<cpf>', methods=['GET'])
def get(cpf: str):
    resident = service.get_by_cpf(cpf)
    return jsonify(resident), 200

@resident_bp.route('/register', methods=['POST'])
def create():
    data = request.get_json()
    resident_request = ResidentRequest.from_dict(data)
    registered_resident = service.create(resident_request)
    return jsonify(registered_resident), 200

@resident_bp.route('/update/<int:id>', methods=['PUT'])
def update(id: int):
    data = request.get_json()
    resident_request = ResidentRequest.from_dict(data)
    updated_resident = service.update(id, resident_request)
    if not updated_resident:
        return jsonify({'error': 'Resident not found'}), 404
    return jsonify(updated_resident), 200

@resident_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete(id: int):
    is_deleted = service.delete(id)
    if is_deleted:
        return jsonify({'message': 'Resident deleted successfully'}), 200
    else:
        return jsonify({'error': 'Resident not found'}), 404
