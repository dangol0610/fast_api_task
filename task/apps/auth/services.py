from datetime import datetime, timedelta
from fastapi import HTTPException, status
from passlib.context import CryptContext
from jose import JWTError, jwt

from task.apps.auth.repository import AuthRepository
from task.apps.auth.schemas import AuthRegisterSchema
from task.settings.settings import settings
from task.utils.dependencies import SessionDependency

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
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

    @classmethod
    async def register(cls, data: AuthRegisterSchema, session: SessionDependency):
        data.password = cls.hash_password(data.password)
        return await AuthRepository.register_user(data=data, session=session)

    @classmethod
    async def login(cls, username: str, password: str, session: SessionDependency):
        user = await AuthRepository.get_by_username(username=username, session=session)
        if not user or not cls.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        payload = {"sub": user.username, "email": user.email}
        access_token = cls.create_access_token(payload)
        refresh_token = cls.create_refresh_token(payload)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
