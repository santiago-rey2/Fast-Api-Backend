"""
Schemas para autenticación y usuarios
"""
from typing import Annotated, Optional
from pydantic import BaseModel, Field, EmailStr

# ==================== USUARIOS ====================

class UserBase(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: Annotated[str, Field(min_length=6, max_length=100)]
    is_admin: bool = False

class UserUpdate(BaseModel):
    username: Optional[Annotated[str, Field(min_length=3, max_length=50)]] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    password: Optional[Annotated[str, Field(min_length=6, max_length=100)]] = None

class UserOut(UserBase):
    id: int
    is_admin: bool
    model_config = {"from_attributes": True}

# ==================== AUTENTICACIÓN ====================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class UserInToken(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
