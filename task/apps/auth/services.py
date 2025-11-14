from datetime import datetime, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt

from task.apps.auth.repository import AuthRepository
from task.apps.auth.schemas import AuthRegisterSchema
from task.settings.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    async def register(self, data: AuthRegisterSchema):
        data.password = self.hash_password(data.password)
        return await self.repository.register_user(data)

    async def login(self, username: str, password: str):
        user = await self.repository.get_by_username(username)
        if not user or not self.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        payload = {"sub": user.username, "email": user.email}
        access_token = self.create_access_token(payload)
        refresh_token = self.create_refresh_token(payload)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
