from flask import Blueprint, request, jsonify
from model.resident import Resident
from config.db_config import db
from service.address_service import AddressService
from service.resident_service import ResidentService
from repository.resident_repository import ResidentRepository
from config.const_config import BASE_URL

resident_bp = Blueprint('residentservice = ResidentService(ResidentRepository())', __name__, url_prefix=f'/{BASE_URL}/residents')

service = ResidentService(ResidentRepository())

@resident_bp.route('', methods=['GET'])
def list():
    residents = service.get_all()
    return jsonify(residents), 200

@resident_bp.route('/<cpf>', methods=['GET'])
def get(cpf: str):
    resident = service.get_by_cpf(cpf)
    if not resident:
        return jsonify({'error': 'morador não encontrado'}), 404
    return jsonify(resident), 200

@resident_bp.route('', methods=['POST'])
def create():
    data = request.get_json()
    resident = Resident(**data)
    registered_resident = service.create(resident)
    return jsonify(registered_resident), 200

@resident_bp.route('/<int:resident_id>', methods=['PUT'])
def update(resident_id: int):
    data = request.get_json()
    updated_resident = service.update(resident_id, data)
    if not updated_resident:
        return jsonify({'error': 'morador não encontrado'}), 404
    return jsonify(updated_resident), 200

@resident_bp.route('/<int:resident_id>', methods=['DELETE'])
def delete(resident_id: int):
    is_deleted = service.delete(resident_id)
    if not is_deleted:
        return jsonify({'error': 'morador não encontrado'}), 404
    return jsonify({'message': 'morador excluído com sucesso'}), 200
