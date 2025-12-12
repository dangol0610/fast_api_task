from datetime import datetime, timedelta
from jose import JWTError, jwt

from task.settings.settings import settings
from task.utils.exceptions import InvalidTokenException


class TokenUtils:
    @staticmethod
    def create_access_token(data: dict, expires_minutes: int = 30):
        expire = datetime.now() + timedelta(minutes=expires_minutes)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, key=settings.SECRET_KEY, algorithm=settings.ALG
        )
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict, expires_days: int = 14):
        expire = datetime.now() + timedelta(days=expires_days)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, key=settings.SECRET_KEY, algorithm=settings.ALG
        )
        return encoded_jwt

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms=settings.ALG
            )
            return payload
        except JWTError:
            raise InvalidTokenException
