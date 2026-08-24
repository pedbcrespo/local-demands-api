from flask import Flask
from flask_restx import Api
from config.db_config import init_db
from config.const_config import BASE_URL
from controller import address_ns, demand_ns, resident_ns

def create_app(config_override=None):
    app = Flask(__name__)
    if config_override:
        app.config.update(config_override)

    init_db(app)

    api = Api(app, title='Local Demands API', version='1.0',
              description='API de demandas locais', doc=f'/{BASE_URL}/docs')
    api.add_namespace(address_ns, path=f'/{BASE_URL}/address')
    api.add_namespace(demand_ns, path=f'/{BASE_URL}/demands')
    api.add_namespace(resident_ns, path=f'/{BASE_URL}/residents')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)