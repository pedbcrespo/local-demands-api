from urllib import response

from flask import request
from flask_restx import Namespace, Resource, fields
from model.request import AddressRequest
from service import AddressService
from repository import AddressRepository, DemandRepository, ResidentRepository

address_ns = Namespace('address', description='Operações relacionadas a endereços')

service = AddressService(AddressRepository(), DemandRepository(), ResidentRepository())

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
