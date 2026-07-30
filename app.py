from flask import Flask
from config.db_config import init_db
from model.address import Address
from controller import address_bp, demand_bp, resident_bp

app = Flask(__name__)
init_db(app)

app.register_blueprint(address_bp)
app.register_blueprint(demand_bp)
app.register_blueprint(resident_bp)

if __name__ == '__main__':
    app.run(debug=True)