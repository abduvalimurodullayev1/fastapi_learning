import time
import jwt
from decouple import config

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}
