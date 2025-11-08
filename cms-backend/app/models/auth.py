"""Authentication models"""
from pydantic import BaseModel


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Data stored in JWT token"""
    username: str | None = None


class User(BaseModel):
    """User model"""
    username: str
    disabled: bool = False


class UserInDB(User):
    """User model with hashed password"""
    hashed_password: str


class LoginRequest(BaseModel):
    """Login request"""
    username: str
    password: str
