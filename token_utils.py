import jwt
import datetime

SECRET_KEY = 'ziye993'

def generate_token(username):
    now = datetime.datetime.utcnow()
    expiration_time = now + datetime.timedelta(hours=1)

    payload = {
        'username': username,
        'iat': now,
        'exp': expiration_time,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token'}
