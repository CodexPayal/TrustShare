from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ForgotPassword(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    token: str
    new_password: str


class MFAEnableResponse(BaseModel):
    message: str
    secret: str
    qr_code: str


class MFAVerify(BaseModel):
    code: str

class MFAChallenge(BaseModel):
    mfa_token: str
    code: str