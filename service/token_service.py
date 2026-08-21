from config.const_config import SECRET_KEY
from model.resident import Resident
from datetime import datetime, timedelta, timezone
import jwt

class TokenService:
    @staticmethod
    def generate_token(resident: Resident) -> str:
        payload = {
            'id': resident.id,
            'cpf': resident.cpf,
            'exp': datetime.now(timezone.utc) + timedelta(hours=8)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def validate_request(token: str) -> bool:
        payload = TokenService.decode_token(token)
        return 'error' not in payload

    @staticmethod
    def get_id(token: str):
        payload = TokenService.decode_token(token)
        if 'error' in payload:
            return None
        return payload.get('id')