from typing import Union, Any
from datetime import timedelta, datetime
import jwt
from config import settings


def verify_password(username, password):
    if username == settings.USERNAME_AUTH and password == settings.PASSWORD_AUTH:
        return True
    return False


def generate_token(username: Union[str, Any], password: Union[str, Any]) -> str:
    expire = int((datetime.now() + timedelta(
        seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )).strftime("%Y%m%d%H%M%S"))
    to_encode = {
        "exp": expire, "username": username, "password": password
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt
