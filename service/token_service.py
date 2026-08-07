from config.const_config import SECRET_KEY
from model.resident import Resident
from datetime import datetime, timedelta, timezone
import jwt

class TokenService:
    @staticmethod
    def generate_token(resident: Resident) -> str:
        payload = {
            'id': resident.id,
            'type': resident.type,
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
    def validate_request(self, token: str) -> bool:
        payload = self.token_service.decode_token(token)
        return 'error' not in payload and payload['type'] == 'resident'