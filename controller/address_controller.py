from flask import request
from flask_restx import Namespace, Resource, fields
from model.request import AddressRequest
from service import AddressService
from repository import AddressRepository, DemandRepository

address_ns = Namespace('address', description='Operações relacionadas a endereços')

service = AddressService(AddressRepository(), DemandRepository())

address_request_model = address_ns.model('AddressRequest', {
    'street': fields.String(required=True, description='Rua'),
    'district': fields.String(required=True, description='Bairro'),
    'city': fields.String(required=True, description='Cidade'),
    'state': fields.String(required=True, description='UF, ex: RJ'),
})

address_response_model = address_ns.model('AddressResponse', {
    'id': fields.Integer(readonly=True),
    'street': fields.String,
    'district': fields.String,
    'city': fields.String,
    'state': fields.String,
})

error_model = address_ns.model('Error', {
    'error': fields.String,
})

message_model = address_ns.model('Message', {
    'message': fields.String,
})

city_response = address_ns.model('CityResponse', {
    'state_code': fields.String,
    'city_name': fields.String
})
@address_ns.route('/all')
class AddressList(Resource):
    @address_ns.marshal_list_with(address_response_model, code=200)
    @address_ns.response(400, 'Não foi possível obter os endereços', error_model)
    def get(self):
        """Lista todos os endereços cadastrados"""
        addresses = service.get_all()
        if addresses is None:
            address_ns.abort(400, 'Could not get the addresses')
        return addresses, 200

@address_ns.route('/state/<state>')
@address_ns.param('state', 'Sigla do estado, ex: RJ')
class CityList(Resource):
    @address_ns.marshal_list_with(city_response, code=200)
    @address_ns.response(400, 'Não foi possível obter as cidades', error_model)
    def get(self, state: str):
        """Lista os nomes das cidades cadastradas para um estado"""
        cities = service.get_cities_by_state(state)
        if cities is None:
            address_ns.abort(400, 'Could not get the cities')
        return cities, 200


@address_ns.route('/register')
class AddressRegister(Resource):
    @address_ns.expect(address_request_model, validate=True)
    @address_ns.marshal_with(address_response_model, code=200)
    @address_ns.response(400, 'Erro ao registrar endereço', error_model)
    def post(self):
        """Registra um novo endereço"""
        data = request.get_json(silent=True)
        address_request = AddressRequest.from_dict(data)
        if not address_request:
            address_ns.abort(400, 'JSON inválido')
        address = service.create(address_request)
        if address is None:
            address_ns.abort(400, 'Could not register address')
        return address


@address_ns.route('/delete/<int:address_id>')
@address_ns.param('address_id', 'ID do endereço a ser deletado')
class AddressDelete(Resource):
    @address_ns.response(200, 'Endereço deletado com sucesso', message_model)
    @address_ns.response(400, 'Endereço não pode ser deletado', error_model)
    def delete(self, address_id: int):
        """Deleta um endereço (falha se ainda estiver em uso por alguma demanda/morador)"""
        is_deleted = service.delete(address_id)
        if not is_deleted:
            address_ns.abort(400, 'Address could not be deleted, it is likely still in use.')
        return {'message': 'Address deleted!'}, 200