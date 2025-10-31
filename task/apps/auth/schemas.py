from pydantic import BaseModel, EmailStr


class AuthSchema(BaseModel):
    username: str
    password: str


class AuthRegisterSchema(AuthSchema):
    email: EmailStr


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
