from flask import Blueprint, request, jsonify
from service.address_service import AddressService
from service.resident_service import ResidentService
from repository.resident_repository import ResidentRepository
from config.const_config import BASE_URL

resident_bp = Blueprint('residentservice = ResidentService(ResidentRepository())', __name__, url_prefix=f'/{BASE_URL}/residents')

service = ResidentService(ResidentRepository())


@resident_bp.route('', methods=['GET'])
def list_residents():
    residents = service.get_all()
    return jsonify(residents), 200


@resident_bp.route('/<cpf>', methods=['GET'])
def get_resident(cpf):
    resident = service.get_by_cpf(cpf)
    if not resident:
        return jsonify({'error': 'morador não encontrado'}), 404
    return jsonify(resident), 200
