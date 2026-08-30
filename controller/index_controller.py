from flask import Blueprint, redirect
from config.const_config import BASE_URL

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    return redirect(f'/{BASE_URL}/docs')

@index_bp.route('/local-deamands')
def index_2():
    return redirect(f'/{BASE_URL}/docs')