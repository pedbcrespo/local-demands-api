from flask import request
from flask_restx import Namespace, Resource, fields
from model.request.resident_request import ResidentRequest
from service.resident_service import ResidentService
from repository.resident_repository import ResidentRepository

resident_ns = Namespace('resident', description='Operações relacionadas aos moradores')
service = ResidentService(ResidentRepository())

resident_request_model = resident_ns.model('ResidentRequest', {
    'full_name': fields.String(required=True, description='Nome completo'),
    'cpf': fields.String(required=True, description='CPF'),
    'phone': fields.String(required=True, description='Telefone'),
    'address_id': fields.Integer(required=True, description='O identificador do endereço do morador'),
})

resident_address_model = resident_ns.model('ResidentAddress', {
    'id': fields.Integer(readonly=True),
    'street': fields.String,
    'district': fields.String,
    'city': fields.String,
    'state': fields.String,
})

resident_response_model = resident_ns.model('ResidentResponse', {
    'id': fields.Integer(readonly=True),
    'full_name': fields.String,
    'cpf': fields.String,
    'phone': fields.String,
    'address': fields.Nested(resident_address_model),
})

error_model = resident_ns.model('Error', {
    'error': fields.String,
})

message_model = resident_ns.model('Message', {
    'message': fields.String,
})


@resident_ns.route('/<cpf>')
@resident_ns.param('cpf', 'CPF do morador (somente números)')
class ResidentGet(Resource):
    @resident_ns.marshal_with(resident_response_model, code=200)
    @resident_ns.response(404, 'Morador não encontrado', error_model)
    def get(self, cpf: str):
        """Busca um morador pelo CPF"""
        resident = service.get_by_cpf(cpf)
        if not resident:
            resident_ns.abort(404, 'Resident not found')
        return resident


@resident_ns.route('/register')
class ResidentCreate(Resource):
    @resident_ns.expect(resident_request_model, validate=True)
    @resident_ns.marshal_with(resident_response_model, code=200)
    @resident_ns.response(400, 'Erro ao registrar morador', error_model)
    def post(self):
        """Registra um novo morador"""
        data = request.get_json()
        resident_request = ResidentRequest.from_dict(data)
        registered_resident = service.create(resident_request)
        if not registered_resident:
            resident_ns.abort(400, 'Could not register resident')
        return registered_resident


@resident_ns.route('/update/<int:id>')
@resident_ns.param('id', 'ID do morador a ser atualizado')
class ResidentUpdate(Resource):
    @resident_ns.expect(resident_request_model, validate=True)
    @resident_ns.marshal_with(resident_response_model, code=200)
    @resident_ns.response(400, 'Erro ao atualizar morador', error_model)
    def put(self, id: int):
        """Atualiza os dados de um morador"""
        data = request.get_json()
        resident_request = ResidentRequest.from_dict(data)
        updated_resident = service.update(id, resident_request)
        if not updated_resident:
            resident_ns.abort(400, 'Could not update the resident')
        return updated_resident


@resident_ns.route('/delete/<int:id>')
@resident_ns.param('id', 'ID do morador a ser deletado')
class ResidentDelete(Resource):
    @resident_ns.response(200, 'Morador deletado com sucesso', message_model)
    @resident_ns.response(400, 'Erro ao deletar morador', error_model)
    def delete(self, id: int):
        """Deleta um morador"""
        is_deleted = service.delete(id)
        if not is_deleted:
            resident_ns.abort(400, 'Could not delete the resident')
        return {'message': 'Resident deleted successfully'}, 200