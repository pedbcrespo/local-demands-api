from flask import request
from flask_restx import Namespace, Resource, fields
from repository.demand_repository import DemandRepository
from repository.address_repository import AddressRepository
from repository.resident_repository import ResidentRepository
from service.demand_service import DemandService
from model.request.demand_request import DemandRequest

demand_ns = Namespace('demand', description='Operações relacionadas a demandas')
service = DemandService(DemandRepository(), AddressRepository(), ResidentRepository())

demand_request_model = demand_ns.model('DemandRequest', {
    'title': fields.String(required=True, description='Titulo da demanda'),
    'description': fields.String(required=True, description='Descrição da demanda'),
    'type': fields.String(required=True, description='O tipo da demanda, ex: Estrutural, Periodica, Emergencial'),
    'resident_id': fields.Integer(required=True, description='O identificador do morador'),
})

demand_address_model = demand_ns.model('DemandAddress', {
    'id': fields.Integer(readonly=True),
    'street': fields.String,
    'district': fields.String,
    'city': fields.String,
    'state': fields.String,
})

demand_response_model = demand_ns.model('DemandResponse', {
    'id': fields.Integer(readonly=True),
    'title': fields.String,
    'description': fields.String,
    'address': fields.Nested(demand_address_model),
    'resident': fields.String,
    'status': fields.String,
    'type': fields.String,
    'created_at': fields.String,
})

error_model = demand_ns.model('Error', {
    'error': fields.String,
})

message_model = demand_ns.model('Message', {
    'message': fields.String,
})


@demand_ns.route('')
class Demand(Resource):
    @demand_ns.marshal_list_with(demand_response_model, code=200)
    @demand_ns.response(400, 'Não foi possível obter as demandas', error_model)
    def get(self):
        """Lista todas as demandas registradas"""
        demands = service.get_all()
        if demands is None:
            demand_ns.abort(400, 'Could not get the demands')
        return demands, 200

    @demand_ns.expect(demand_request_model, validate=True)
    @demand_ns.marshal_with(demand_response_model, code=200)
    @demand_ns.response(400, 'Erro ao registrar demanda', error_model)
    def post(self):
        """Registra uma nova demanda"""
        data = request.get_json()
        demand_request = DemandRequest.from_dict(data)
        demand = service.create(demand_request)
        if not demand:
            demand_ns.abort(400, 'Could not register demand')
        return demand

@demand_ns.route('/types')
class DemandType(Resource):
    @demand_ns.response(200, 'Lista de nomes dos tipos de demandas, ex: ["STRUCTURAL", "EMERGENCY", ...]')
    @demand_ns.response(400, 'Não foi possível obter os tipos de demandas', error_model)
    def get(self):
        """Lista todas as demandas registradas"""
        demands = service.get_all_demand_types()
        if demands is None:
            demand_ns.abort(400, 'Could not get the demand types')
        return demands, 200

@demand_ns.route('/<int:demand_id>/finish')
@demand_ns.param('demand_id', 'ID da demanda a ser marcada como finalizada')
class DemandFinish(Resource):
    @demand_ns.marshal_with(demand_response_model, code=200)
    @demand_ns.response(400, 'Demanda não pode ser finalizada', error_model)
    def put(self, demand_id: int):
        """Finaliza a demanda. Ao final do processo, a mesma não pode mais ser alterada"""
        response = service.finish(demand_id)
        if not response:
            demand_ns.abort(400, 'Demand could not be finished')
        return response


@demand_ns.route('/<int:demand_id>/delete')
@demand_ns.param('demand_id', 'ID da demanda a ser deletada')
class DemandDelete(Resource):
    @demand_ns.response(200, 'Demanda deletada com sucesso', message_model)
    @demand_ns.response(400, 'Demanda não pode ser deletada', error_model)
    def delete(self, demand_id: int):
        """Deleta uma demanda"""
        success = service.delete(demand_id)
        if not success:
            demand_ns.abort(400, 'Demand could not be deleted')
        return {'message': 'Demand deleted successfully'}, 200